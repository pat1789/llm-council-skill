"""Assemble rapport.html et transcript.md d'une session du Council Brevet.
Usage : python3 -I build_report.py <dossier_session> <template.html>"""
import re, subprocess, sys, os, html, datetime

S, TPL = sys.argv[1], sys.argv[2]
rd = lambda p: open(os.path.join(S, p), encoding="utf-8").read()

def md2html(md):
    return subprocess.run(["pandoc", "-f", "gfm", "-t", "html"], input=md, capture_output=True, text=True, check=True).stdout

def section(md, title):
    m = re.search(r"^## " + re.escape(title) + r".*?$\n(.*?)(?=^## |\Z)", md, re.S | re.M)
    return m.group(1).strip() if m else ""

css = re.search(r"<style>.*?</style>", open(TPL, encoding="utf-8").read(), re.S).group(0)
script = re.search(r"<script>.*?</script>", open(TPL, encoding="utf-8").read(), re.S).group(0)

ch = rd("07_synthese-chairman.md")
mods = rd("08_modifications.md")
sout = rd("09_soutenance.md")
formel = rd("03_controle-formel.md")

# fiches de modifications
parts = re.split(r"(?=^### M-\d+)", mods, flags=re.M)
head, fiches = parts[0], parts[1:]
recap = ""
if fiches:
    last = fiches[-1]
    k = re.search(r"^#{2,3} (?!M-).*$", last, re.M)
    if k:
        recap, fiches[-1] = last[k.start():], last[:k.start()]
counts = {"critique": 0, "importante": 0, "secondaire": 0}
fiche_html = []
for f in fiches:
    pm = re.search(r"Priorit[ée]\s*\|\s*\**\s*(critique|importante|secondaire)", f, re.I)
    p = pm.group(1).lower() if pm else "secondaire"
    counts[p] += 1
    title = f.splitlines()[0].lstrip("# ").strip()
    body = md2html("\n".join(f.splitlines()[1:]))
    fiche_html.append(f'<article class="card fiche" data-p="{p}"><h3>{html.escape(title)} '
                      f'<span class="tag {p}">{p}</span></h3><div class="table-wrap">{body}</div></article>')

def det(summary, md):
    return f"<details><summary>{html.escape(summary)}</summary><div>{md2html(md)}</div></details>"

roles = {"A": "A — Expert des exigences du brevet", "B": "B — Méthodologie, structure, rédaction",
         "C": "C — Expert du domaine professionnel", "D": "D — Examinateur critique", "E": "E — Coach stratégique"}
analyses = "".join(det(roles[l], rd(f"04_conseillers/{l}.md")) for l in "ABCDE")
relect = rd("05_relectures/_correspondance.md") + "\n\n" + "\n\n---\n\n".join(
    rd(f"05_relectures/relecteur-{i}.md") for i in range(1, 6))

est = section(ch, "Estimation indicative")
today = datetime.date.today().isoformat()
page = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rapport Council Brevet</title>{css}
<style>.card table{{font-size:.9rem}} .card h2,.card h3{{margin-top:12px}}</style></head>
<body><main>
<header><h1>Rapport du Council — Dossier de performance</h1>
<div class="meta">Brevet fédéral « Spécialiste en gestion de PME » · option PME familiales · Version analysée : V1 (en cours de rédaction) · Session : 2026-11-15 · Rapport généré le {today}</div></header>
<div class="card disclaimer"><strong>Document confidentiel, local — ne pas diffuser.</strong>
Les points sont une <strong>estimation indicative du Council, non officielle</strong>. Seuls les experts aux examens notent le dossier.
Étiquettes : <strong>[FAIT]</strong> vérifiable (avec page) · <strong>[HYPOTHÈSE]</strong> interprétation · <strong>[RECOMMANDATION]</strong> conseil du Council.
« Exigence officielle » = A1, A2, A3 ou Directives ; tout le reste est une recommandation.</div>
<h2>Verdict</h2><div class="card">{md2html(section(ch, "Verdict"))}</div>
<div class="kpis">
<div class="card kpi"><div class="v">{counts['critique']}</div><div class="l">Modifications critiques</div></div>
<div class="card kpi"><div class="v">{counts['importante']}</div><div class="l">Modifications importantes</div></div>
<div class="card kpi"><div class="v">{counts['secondaire']}</div><div class="l">Modifications secondaires</div></div>
<div class="card kpi"><div class="v">27.01.2027</div><div class="l">Délai de dépôt (à confirmer dans la publication)</div></div>
</div>
<h2>Estimation indicative</h2><div class="card">{md2html(est)}</div>
<h2>Contrôle formel</h2><div class="card table-wrap">{md2html(formel.split(chr(10), 2)[2] if formel.count(chr(10)) > 2 else formel)}</div>
<h2>Évaluation critère par critère</h2><div class="card table-wrap">{md2html(section(ch, "Évaluation critère par critère"))}</div>
<h2>Synthèse du Chairman</h2>
<h3>Améliorations prioritaires</h3><div class="card">{md2html(section(ch, "Améliorations prioritaires"))}</div>
<h3>Risques d'échec</h3><div class="card">{md2html(section(ch, "Risques d'échec"))}</div>
<h3>Points forts</h3><div class="card">{md2html(section(ch, "Points forts"))}</div>
<h3>Points faibles</h3><div class="card">{md2html(section(ch, "Points faibles"))}</div>
<h3>Critères insuffisamment démontrés</h3><div class="card">{md2html(section(ch, "Critères insuffisamment démontrés"))}</div>
<h3>Incohérences</h3><div class="card">{md2html(section(ch, "Incohérences"))}</div>
<h3>Exposition à l'oral</h3><div class="card">{md2html(section(ch, "Exposition à l'oral"))}</div>
<h3>Désaccords du Council et arbitrage</h3><div class="card">{md2html(section(ch, "Désaccords du Council"))}</div>
<h2>Modifications recommandées</h2>
<div class="filters" role="group" aria-label="Filtrer par priorité">
<button type="button" data-f="all" aria-pressed="true">Toutes ({len(fiches)})</button>
<button type="button" data-f="critique" aria-pressed="false">Critiques ({counts['critique']})</button>
<button type="button" data-f="importante" aria-pressed="false">Importantes ({counts['importante']})</button>
<button type="button" data-f="secondaire" aria-pressed="false">Secondaires ({counts['secondaire']})</button></div>
{''.join(fiche_html)}
{('<h3>Récapitulatif</h3><div class="card table-wrap">' + md2html(recap) + '</div>') if recap else ''}
<h2>Préparation à la soutenance</h2>{det("Ouvrir la préparation complète (questions du jury, réponses attendues, contradictions, plan de présentation)", sout)}
<h2>Détail des travaux du Council</h2>{analyses}
{det("Relectures croisées anonymes (correspondance révélée)", relect)}
{det("Vérification des preuves", rd("06_constats-verifies.md"))}
<footer>Sources officielles : A1 (17.06.2024), Directives (24.06.2022), Profil professionnel (17.03.2016), A2 (17.03.2016), A3 (25.10.2019).
Le mémoire original n'a pas été modifié (empreintes : 00_empreintes.txt). Généré par le LLM Council, mode Brevet fédéral.</footer>
</main>{script}</body></html>"""
open(os.path.join(S, "rapport.html"), "w", encoding="utf-8").write(page)

# transcript
tr = ["# Transcript complet — Council Brevet, session 2026-11-15 (V1)\n",
      "## Contexte\n", open(os.path.join(S, "../../00_contexte/contexte-candidat.md"), encoding="utf-8").read(),
      "\n## Inventaire\n", open(os.path.join(S, "../_inventaire-2026-11-15.md"), encoding="utf-8").read(),
      "\n## Empreintes\n```\n" + rd("00_empreintes.txt") + "```\n",
      "\n## Plan mesuré\n", rd("02_plan.md"), "\n## Contrôle formel\n", formel]
for l in "ABCDE":
    tr += [f"\n## Analyse {roles[l]}\n", rd(f"04_conseillers/{l}.md")]
tr += ["\n## Relectures croisées\n", relect, "\n## Vérification des preuves\n", rd("06_constats-verifies.md"),
       "\n## Synthèse du Chairman\n", ch, "\n## Modifications\n", mods, "\n## Préparation à la soutenance\n", sout]
open(os.path.join(S, "transcript.md"), "w", encoding="utf-8").write("\n".join(tr))
print("fiches:", len(fiches), counts)
