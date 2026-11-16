"""Vérifie que chaque citation « … » des analyses existe dans le texte paginé.
Usage : python3 -I verif_citations.py <texte-pagine.md> <fichier1.md> [...]
Sortie : tableau Markdown (fichier, constat, page annoncée, statut, page trouvée)."""
import re, sys, unicodedata

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"-\s*\n\s*", "", s)          # césures
    s = re.sub(r"[\s ]+", " ", s)
    return s.strip().lower()

text = open(sys.argv[1], encoding="utf-8").read()
pages = {}
for m in re.finditer(r"=== PAGE PDF (\d+) \(p\. imprimée (\d+)\) ===\n(.*?)(?==== PAGE PDF|\Z)", text, re.S):
    pages[int(m.group(2))] = norm(m.group(3))
allnorm = " ".join(pages[k] for k in sorted(pages))

print("| Fichier | Constat | Page annoncée | Statut | Page trouvée | Extrait |")
print("|---|---|---|---|---|---|")
for f in sys.argv[2:]:
    cur = "?"
    page_annoncee = None
    for line in open(f, encoding="utf-8"):
        h = re.match(r"#+\s*((?:K|M)-\d+)", line)
        if h:
            cur, page_annoncee = h.group(1), None
        pm = re.search(r"p\.\s*(\d+)", line) if re.search(r"^\s*[-*]?\s*\**Page", line) else None
        if pm:
            page_annoncee = int(pm.group(1))
        if not re.search(r"Passage\s*:", line):
            continue
        for q in re.findall(r"«\s*(.+?)\s*»", line):
            nq = norm(q)
            # tolère les coupures [...] ou … dans la citation
            parts = [p.strip() for p in re.split(r"\[\s*(?:…|\.\.\.)\s*\]|…|\.\.\.", nq) if len(p.strip()) >= 12]
            if not parts:
                continue
            found = [k for k, t in pages.items() if all(p in t for p in parts)]
            if not found and all(p in allnorm for p in parts):
                statut, fp = "vérifié (à cheval sur 2 pages)", "-"
            elif not found:
                statut, fp = "INTROUVABLE", "-"
            elif page_annoncee in found or (page_annoncee and page_annoncee + 1 in found) or (page_annoncee and page_annoncee - 1 in found):
                statut, fp = "vérifié", ",".join(map(str, found))
            else:
                statut, fp = "page corrigée", ",".join(map(str, found))
            name = f.rsplit("/", 1)[-1]
            print(f"| {name} | {cur} | {page_annoncee} | {statut} | {fp} | {q[:60].replace('|','/')} |")
