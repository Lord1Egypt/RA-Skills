#!/usr/bin/env python3
"""
Aide à la PASSE VISION du rapprochement.

`main.py` signale, dans chaque `clients/<slug>/needs_vision.json`, les documents
que l'extraction déterministe ne lit pas de façon fiable (relevé dont les soldes
ne se réconcilient pas, facture dont HT+TVA≠TTC, PDF scanné sans couche texte…).
Ces documents DOIVENT être relus en vision : l'agent ouvre les images des pages
et écrit, à côté du PDF, un sidecar `<pdf>.vision.json` corrigé — que main.py
reprendra ensuite comme AUTORITÉ (puis re-contrôlera via le même gate).

Ce script ne « voit » rien lui-même (il n'est pas un modèle) : il prépare le
travail et le rend trivial pour l'agent. Pour chaque document signalé, il
produit, via `extract.py --vision-kit`, les images des pages + un squelette de
sidecar pré-rempli au bon schéma.

Usage :
  python3 resolve_vision.py [<racine_clients>]    (défaut : ./clients)

Sortie (JSON sur stdout) : la liste des kits à traiter
  [{ "client", "source_file", "reason", "sidecar_path", "images":[...],
     "skeleton": {...}, "current_extraction": {...} }]

Marche à suivre pour l'agent :
  1. Lancer ce script → obtenir les kits.
  2. Pour chaque kit : lire les images (outil Read), corriger le `skeleton`
     (montants SIGNÉS : crédit +, débit − ; champs illisibles = null, JAMAIS
     inventés ; pour un relevé, vérifier ouverture + Σ montants = clôture).
  3. Sauver le squelette corrigé tel quel dans `sidecar_path`.
  4. Relancer `python3 main.py <racine_clients>` : les sidecars font autorité,
     et un sidecar qui ne réconcilie toujours pas est RE-signalé (jamais trusté
     en silence).
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXTRACT = HERE / "extract.py"
PY = sys.executable or "python3"


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


def vision_kit(pdf_path, out_dir):
    """Appelle `extract.py --vision-kit` : rend les images des pages + squelette."""
    res = subprocess.run([PY, str(EXTRACT), str(pdf_path), "--vision-kit", str(out_dir)],
                         capture_output=True, text=True)
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        return {"error": res.stderr.strip() or "vision-kit illisible"}


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("clients")
    if not root.exists():
        print(json.dumps({"error": f"racine introuvable : {root}"}))
        sys.exit(1)

    kits = []
    for client_dir in sorted(d for d in root.iterdir() if d.is_dir() and not d.name.startswith("_")):
        queue = load_json(client_dir / "needs_vision.json", [])
        for entry in queue if isinstance(queue, list) else []:
            src = entry.get("source_file")
            if not src or not Path(src).exists():
                continue
            img_dir = Path(tempfile.mkdtemp(prefix="vision_"))
            kit = vision_kit(src, img_dir)
            kits.append({
                "client": client_dir.name,
                "source_file": src,
                "reason": entry.get("reason"),
                "sidecar_path": kit.get("sidecar_path", str(src) + ".vision.json"),
                "images": kit.get("images", []),
                "skeleton": kit.get("skeleton"),
                "current_extraction": kit.get("current_extraction"),
            })

    print(json.dumps(kits, ensure_ascii=False, indent=2))
    n = len(kits)
    if n:
        print(f"\n{n} document(s) à relire en vision. Pour chacun : lire les images, "
              f"corriger le squelette, sauver dans sidecar_path, puis relancer main.py.",
              file=sys.stderr)
    else:
        print("\nAucun document à relire en vision. ✅", file=sys.stderr)


if __name__ == "__main__":
    main()
