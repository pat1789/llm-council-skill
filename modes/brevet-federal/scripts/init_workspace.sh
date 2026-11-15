#!/usr/bin/env bash
# Crée l'espace de travail confidentiel du mode Brevet fédéral.
# Usage : bash init_workspace.sh [répertoire-parent]   (défaut : répertoire courant)
# Idempotent : ne remplace jamais un fichier existant.
set -euo pipefail

MODE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PARENT="${1:-$PWD}"
WS="$PARENT/brevet-council"

case "$WS" in
  "$MODE_DIR"/*|"$(dirname "$(dirname "$MODE_DIR")")"/brevet-council)
    echo "Refus : l'espace de travail ne doit pas être créé dans le dossier du skill." >&2
    echo "Lancez le script depuis votre dossier de projet." >&2
    exit 1 ;;
esac

mkdir -p "$WS"/{00_contexte,01_references-officielles,02_memoire/original,02_memoire/versions,03_annexes,04_soutenance,05_sessions}

# Rien de cet espace ne doit jamais entrer dans un dépôt git.
[ -f "$WS/.gitignore" ] || printf '# Confidentiel : rien ici ne doit être versionné.\n*\n' > "$WS/.gitignore"

copy_if_absent() { [ -e "$2" ] || cp "$1" "$2"; }
copy_if_absent "$MODE_DIR/templates/contexte-candidat.md"   "$WS/00_contexte/contexte-candidat.md"
copy_if_absent "$MODE_DIR/templates/suivi-corrections.csv"  "$WS/suivi-corrections.csv"

if [ ! -f "$WS/LISEZMOI.md" ]; then
cat > "$WS/LISEZMOI.md" <<'EOF'
# Espace de travail — Council Brevet fédéral (confidentiel)

| Dossier | À déposer |
|---|---|
| 00_contexte/ | Remplir `contexte-candidat.md` |
| 01_references-officielles/ | A1, Directives, Profil professionnel, A2, A3, règlement d'examen, publication de la session |
| 02_memoire/original/ | Votre dossier de performance actuel (PDF ; + Word si possible). Ne sera jamais modifié. |
| 02_memoire/versions/ | Plus tard : v2, v3… après corrections (ex. `v2_2026-12-10.pdf`) |
| 03_annexes/ | Annexes, si elles ne sont pas dans le PDF |
| 04_soutenance/ | Support de présentation, consignes reçues |
| 05_sessions/ | Rempli par le Council : un dossier par analyse |
| suivi-corrections.csv | Tableau de suivi : mettez à jour les colonnes Statut et Commentaire candidat |

Quand tout est en place : dites « council brevet inventaire », puis « council brevet go ».
Ce dossier contient un `.gitignore` qui empêche tout envoi vers git.
EOF
fi

echo "Espace de travail prêt : $WS"
