# LLM Council — Mode Brevet fédéral suisse

Mode d'évaluation et de coaching pour le **dossier de performance** (le « mémoire ») de
l'examen professionnel fédéral **« Spécialiste en gestion de PME »** (formation
professionnelle supérieure suisse, organe responsable : Formation Entrepreneurs PME Suisse).

> Il s'agit d'un **brevet fédéral** (diplôme), jamais d'un brevet d'invention.

Ce mode est **indépendant** du Council stratégique décrit dans `SKILL.md`. Il réutilise
la méthode (conseillers indépendants → relecture croisée anonyme → Chairman) mais avec
ses propres conseillers, ses propres règles et ses propres livrables. Rien de ce qui suit
ne s'applique au Council stratégique.

Fichiers du mode :

```
modes/brevet-federal/
├── MODE.md                          ← ce fichier (déroulement)
├── prompts.md                       ← prompts des conseillers, relecteurs, Chairman, etc.
├── reference/referentiel-officiel.md← transcription sourcée de la grille A1 et des directives
├── templates/                       ← modèles copiés dans l'espace de travail du candidat
└── scripts/init_workspace.sh        ← crée l'espace de travail
```

---

## Règles impératives (s'appliquent à chaque étape, à chaque agent)

1. **Ne jamais modifier le mémoire original.** Il est copié, haché (SHA-256) et mis en
   lecture seule. Toute proposition est livrée dans un fichier séparé.
2. **Conserver les versions.** Chaque nouvelle version du mémoire est un nouveau fichier
   (`v2`, `v3`…). Chaque session d'analyse a son propre dossier daté, jamais écrasé.
3. **Ne jamais inventer** de critère officiel, de point, de seuil, de référence
   bibliographique, de chiffre de l'entreprise ou de citation du mémoire.
   Un critère officiel n'est cité que s'il figure dans `referentiel-officiel.md` **et**
   dans le PDF source de `01_references-officielles/`.
4. **Distinguer systématiquement** trois natures d'énoncés, avec ces étiquettes :
   - `[FAIT]` — vérifiable dans un document (mémoire ou référence officielle), avec page.
   - `[HYPOTHÈSE]` — interprétation ou supposition (p. ex. « les experts risquent de… »).
   - `[RECOMMANDATION]` — conseil du Council, sans valeur officielle.
   Et deux sources d'exigences : **« Exigence officielle (A1 p. X) »** vs
   **« Recommandation du Council »**.
5. **Aucune note officielle.** Toute estimation de points porte la mention
   « Estimation indicative du Council — non officielle. Seuls les experts aux examens
   notent le dossier. » et est donnée sous forme de **fourchette**.
6. **Confidentialité.**
   - Les documents restent dans l'espace de travail local `brevet-council/`, qui contient
     un `.gitignore` excluant tout. Ne jamais commiter, pousser, publier (Artifact, Docs,
     Gist…) ni coller le contenu du mémoire dans un service externe.
   - Aucune recherche web contenant des extraits du mémoire, des noms de personnes ou de
     l'entreprise. Une recherche web n'est permise que sur des sujets génériques
     (p. ex. un article de loi), et en le signalant.
   - Les sous-agents reçoivent les documents localement ; on ne leur demande jamais de
     les transmettre ailleurs.
7. **Pas d'analyse sans feu vert.** Tant que le candidat n'a pas confirmé explicitement
   que les documents sont complets (phase 0), aucune analyse de fond n'est lancée.
8. **Mode correction interdit dans le livrable final** (A1 4, p. 12) : les propositions
   sont livrées en texte propre à recopier, jamais sous forme de marques de révision
   dans le fichier qui sera déposé.

---

## Activation

Déclencheurs : « council brevet », « mode brevet », « évalue mon dossier de performance »,
« évalue mon mémoire de brevet », « jury brevet », « prépare ma soutenance de brevet ».

Commandes reconnues dans ce mode :

| Commande | Effet |
|---|---|
| `council brevet init` | Crée l'espace de travail (phase 0a) |
| `council brevet inventaire` | Vérifie les documents présents, sans rien analyser (phase 0b) |
| `council brevet go` (ou confirmation explicite équivalente) | Lance une session complète (phases 1–9) |
| `council brevet suivi` | Met à jour le tableau de suivi à partir d'une nouvelle version, sans session complète |
| `council brevet soutenance` | Relance uniquement la préparation à la soutenance (phase 7) |

---

## Phase 0 — Préparation (aucune analyse)

### 0a. Créer l'espace de travail

Dans le répertoire de travail **du candidat** (pas dans le dossier du skill) :

```bash
bash <chemin-du-skill>/modes/brevet-federal/scripts/init_workspace.sh
```

Résultat :

```
brevet-council/
├── .gitignore                         ← « * » : rien n'est jamais versionné dans git
├── LISEZMOI.md
├── 00_contexte/contexte-candidat.md   ← questionnaire à remplir
├── 01_references-officielles/         ← A1, directives, profil, A2, A3, règlement…
├── 02_memoire/
│   ├── original/                      ← le dossier tel qu'il est aujourd'hui (PDF + .docx si dispo)
│   └── versions/                      ← v2, v3… déposées par le candidat après corrections
├── 03_annexes/                        ← annexes séparées, si elles ne sont pas dans le PDF
├── 04_soutenance/                     ← support de présentation, notes, consignes reçues
├── 05_sessions/                       ← une sous-dossier par analyse, jamais écrasé
└── suivi-corrections.csv              ← tableau maître de suivi (persiste entre sessions)
```

### 0b. Inventaire et liste de contrôle

Lister le contenu de chaque dossier et produire `05_sessions/_inventaire-<date>.md` en
remplissant `templates/checklist-documents.md` :

- **Obligatoire** pour lancer : A1, Directives, mémoire (PDF), contexte-candidat rempli.
- **Fortement recommandé** : Profil professionnel / grille des compétences, version
  Word du mémoire (pour citer des passages exacts), annexes.
- **Nécessaire pour la soutenance** : A2 (présentation), A3 (entretien).
- **Optionnel** : règlement d'examen, publication de la session, retours d'un
  formateur, ancien dossier en cas de répétition.

Vérifier aussi :
- version et date des PDF officiels vs `reference/referentiel-officiel.md` ;
- que le mémoire est lisible (texte extractible — sinon prévoir OCR et le dire) ;
- que `contexte-candidat.md` précise : session visée, langue, **certificat
  supplémentaire PME familiales oui/non**, statut (première tentative / répétition).

### 0c. Point d'arrêt obligatoire

Présenter au candidat l'inventaire (présent / manquant / conséquence) et **s'arrêter**.
Ne passer à la phase 1 que sur confirmation explicite (« go », « tout est là, lance »…).
Si un document obligatoire manque, le dire et ne pas proposer de lancer quand même.
Si A2/A3 manquent, proposer de lancer en précisant que la soutenance sera préparée sans
critères officiels.

---

## Phase 1 — Mise en sécurité et extraction

Créer `05_sessions/AAAA-MM-JJ_vN/` (N = version du mémoire analysée).

1. **Empreinte** : `sha256sum` de chaque fichier du mémoire → `00_empreintes.txt`.
   Mettre `02_memoire/original/` en lecture seule (`chmod -R a-w`).
   En début de toute session ultérieure, recontrôler l'empreinte de l'original ; si elle a
   changé, s'arrêter et prévenir.
2. **Texte paginé** : extraire le texte page par page dans `01_texte-pagine.md`
   avec des marqueurs `=== PAGE <n PDF> (p. imprimée <x>) ===`
   (`pdftotext -layout -f n -l n`). Noter la correspondance page PDF ↔ numéro imprimé :
   **toutes les références de page des livrables utilisent le numéro imprimé** et, entre
   parenthèses, la page PDF.
3. **Plan du mémoire** : relever la table des matières et repérer où commencent
   l'introduction, la partie principale, la conclusion et l'annexe → `02_plan.md`.
4. **Vérification du référentiel** : relire les pages 3–11 de l'A1 fourni et confirmer
   que critères et points correspondent à `referentiel-officiel.md`. Écart → arrêt.

## Phase 2 — Contrôle formel (déterministe, avant les conseillers)

Le non-respect des exigences formelles fait **retourner** le dossier (A1 2.3) : ce
contrôle se fait par mesure, pas par opinion. Produire `03_controle-formel.md` :

| Contrôle | Méthode | Exigence |
|---|---|---|
| Pages intro + principale + conclusion | plan + `pdfinfo` | 25–40 (45 si certificat PME fam.) |
| Pages d'annexe | plan | ≤ 15 |
| Police | `pdffonts` (polices du corps du texte) | Arial (variantes Arial-*/ArialMT) |
| Taille / interligne | inspection de pages types (rendu image si nécessaire) | 11 pt, 1.5 — indiquer « non mesurable avec certitude » si c'est le cas |
| Éléments de structure | plan | couverture, déclaration d'indépendance signée, bref CV, table des matières, intro, partie principale, conclusion, annexe avec inventaire des sources externes |
| Ordre des éléments | plan | ordre A1 2.3 |
| Marques de révision / commentaires | `.docx` si fourni | aucune |

Chaque écart devient une modification de priorité **critique**.

## Phase 3 — Les cinq conseillers (en parallèle, indépendants)

Lancer **en un seul message** 5 sous-agents (`general-purpose`), chacun avec son prompt
de `prompts.md` § 1. Chacun reçoit **les mêmes** entrées :
`01_texte-pagine.md`, `02_plan.md`, `03_controle-formel.md`,
`reference/referentiel-officiel.md`, `00_contexte/contexte-candidat.md`, et le chemin
des PDF officiels pour vérification. Aucun ne voit le travail des autres.

| Conseiller | Rôle |
|---|---|
| **A** | Expert des exigences du brevet fédéral suisse |
| **B** | Expert en méthodologie, structure et rédaction |
| **C** | Expert du domaine professionnel (gestion de PME, et la branche du candidat) |
| **D** | Examinateur critique — erreurs, incohérences, lacunes |
| **E** | Coach stratégique — améliorations à plus fort impact sur la note |

Sortie de chacun : `04_conseillers/<lettre>.md`, au format imposé (constats numérotés
avec page, citation exacte, étiquette FAIT/HYPOTHÈSE/RECOMMANDATION, critère).

## Phase 4 — Relecture croisée anonyme

1. Tirer au sort une correspondance conseiller → « Analyse 1…5 » (consigner dans
   `05_relectures/_correspondance.md`, révélée seulement dans le transcript).
2. Retirer des textes tout indice d'identité (titre du rôle, « en tant que coach… »).
3. Lancer **en parallèle** 5 relecteurs (`prompts.md` § 2). Chacun voit les 5 analyses
   anonymes + le texte paginé + le référentiel, et répond aux cinq questions :
   analyse la plus pertinente · erreurs de raisonnement · points oubliés ·
   désaccords entre experts · risques pouvant pénaliser le mémoire.

## Phase 5 — Vérification des preuves (anti-hallucination)

Avant le Chairman, l'orchestrateur (pas un sous-agent) contrôle **chaque** constat :

- la citation existe-t-elle mot pour mot (à la normalisation des espaces près) dans
  `01_texte-pagine.md`, à la page indiquée ? → `vérifié` / `page corrigée` / `introuvable` ;
- le critère cité existe-t-il dans le référentiel ? → sinon le reclasser en
  « Recommandation du Council ».

Les constats `introuvable` sont écartés (et listés comme tels dans le transcript).
Résultat : `06_constats-verifies.md`.

## Phase 6 — Chairman

Un sous-agent (`prompts.md` § 3) reçoit tout : analyses dés-anonymisées, relectures,
constats vérifiés, contrôle formel, référentiel, contexte, et — s'il existe — le
`suivi-corrections.csv` de la session précédente. Il produit `07_synthese-chairman.md` :

1. Verdict en 5 lignes.
2. **Évaluation critère par critère** (I-1…I-5, P-1…P-13, C-1, C-2, et F-1…F-4 si
   certificat PME fam.) : statut *rempli / partiellement / pas rempli / non démontré*,
   preuves (pages), ce qui manque.
3. Points forts.
4. Points faibles.
5. Critères insuffisamment démontrés.
6. Incohérences (chiffres, dates, rôles, affirmations contradictoires).
7. Risques d'échec (formels éliminatoires d'abord, puis seuil des 18 points).
8. Améliorations prioritaires (top 5, ordonnées par gain de points / effort).
9. **Estimation indicative** : la grille A1 le permet (points par critère, demi-points).
   Donner une fourchette basse / haute, total sur 30, comparaison au seuil de 18,
   avec la mention de non-officialité. Ne jamais l'appeler « note ».
10. Désaccords du Council et arbitrage motivé.
11. Si session précédente : évolution par rapport à la version antérieure.

## Phase 7 — Recommandations de modifications (livrable principal)

Un sous-agent « Rédacteur des modifications » (`prompts.md` § 4) transforme chaque
problème retenu en fiche directement applicable. Chaque fiche contient **obligatoirement** :

| # | Champ |
|---|---|
| 1 | Page (imprimée + PDF) et passage concerné (citation exacte ou description précise de l'emplacement) |
| 2 | Description du problème |
| 3 | Importance : pourquoi cela compte pour l'évaluation |
| 4 | Modification recommandée |
| 5 | Exemple de reformulation ou de contenu à ajouter (prêt à adapter, entre `[crochets]` pour les données que seul le candidat connaît — **jamais** de chiffres inventés) |
| 6 | Priorité : **critique** / **importante** / **secondaire** |
| 7 | Critère officiel concerné (ID + source) ou « aucun — recommandation du Council » |

Définition des priorités :
- **critique** : risque de dossier retourné (formel) ou critère à ≥ 2 points non démontré,
  ou risque de passer sous 18 points ;
- **importante** : critère partiellement rempli, gain de points plausible ;
- **secondaire** : qualité, lisibilité, impression générale ; pas de gain de points direct.

Sortie : `08_modifications.md` (fiches ordonnées critique → secondaire, puis par page)
et mise à jour du suivi (phase 9).

## Phase 8 — Préparation à la soutenance

Sous-agent « Jury » (`prompts.md` § 5), qui reçoit tout le dossier de session.
Rappel officiel : présentation 20 min (10 pts), entretien 60 min (20 pts) ; « les
compétences qui ne sont pas décrites dans le dossier de performance peuvent être
examinées … lors de l'entretien » (A1 2.2). Sans A2/A3, le préciser en tête et ne citer
**aucun** critère officiel d'oral.

Sortie `09_soutenance.md` :
- 15–25 questions difficiles, classées par thème/critère, avec la raison de la question ;
- pour chacune : éléments de réponse attendus, pièges, page du mémoire à maîtriser ;
- liste des chiffres, dates, décisions et modèles à connaître par cœur ;
- contradictions que le jury pourrait relever (avec pages) ;
- compétences non couvertes par le dossier → questions probables à l'entretien.

## Phase 9 — Rapports et suivi

Dans le dossier de session :

| Fichier | Contenu |
|---|---|
| `rapport.html` | Rapport visuel autonome (gabarit `templates/rapport-template.html`) : verdict, contrôle formel, tableau critère par critère avec fourchette, top priorités, toutes les fiches de modification (filtrables par priorité), soutenance, sections repliables pour les analyses et relectures, rappel des règles (faits / hypothèses / recommandations, non-officialité). |
| `transcript.md` | Transcript complet : contexte, inventaire, empreintes, contrôle formel, 5 analyses, correspondance d'anonymisation, 5 relectures, vérification des preuves (y compris constats écartés), synthèse Chairman, modifications, soutenance. |
| `modifications.md` | Copie de `08_modifications.md` — la liste de travail du candidat. |
| `suivi-corrections.csv` | Instantané du tableau de suivi à la date de la session. |

**Tableau de suivi maître** `brevet-council/suivi-corrections.csv`
(format : `templates/suivi-corrections.csv`, séparateur `;`, UTF-8 avec BOM pour Excel) :

- nouvelle fiche → nouvelle ligne `M-NNN`, statut `à faire` ;
- les identifiants ne sont **jamais** réutilisés ; une ligne n'est jamais supprimée ;
- le candidat met à jour `Statut` (`à faire` / `en cours` / `fait` / `refusé`) et
  `Commentaire candidat` ;
- lors d'une session sur une version N+1, le Council vérifie chaque ligne
  `fait` / `en cours` contre la nouvelle version et renseigne `Vérification Council`
  (`résolu` / `partiellement` / `non résolu` / `régression`), avec la version.

Le rapport HTML est un fichier local. Il n'est **pas** publié comme Artifact ni envoyé
ailleurs, sauf demande explicite du candidat après rappel du caractère confidentiel.

## Phase 10 — Compte rendu au candidat

Message court : verdict, fourchette indicative, les 3 modifications critiques, chemins
des fichiers produits, documents manquants éventuels, prochaine étape suggérée.

---

## Itérations (nouvelle version du mémoire)

1. Le candidat dépose `02_memoire/versions/v2_<date>.pdf` (l'original n'est jamais remplacé).
2. `council brevet go` → session `…_v2`, qui reprend le suivi maître et mesure les progrès.
3. `council brevet suivi` pour une vérification rapide des seules corrections, sans
   relancer les cinq conseillers.

## Ce que ce mode ne fait pas

- Il ne rédige pas le mémoire à la place du candidat : les exemples de reformulation
  sont des modèles à adapter avec ses données réelles.
- Il n'invente ni données d'entreprise, ni sources, ni critères d'oral.
- Il ne remplace pas les expertes et experts aux examens, ni l'organe responsable :
  en cas de doute sur une règle, la recommandation est de poser la question au
  secrétariat des examens (FEP Suisse).
