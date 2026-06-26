#!/usr/bin/env python3
"""
Exporte un fichier .vaudtax vers un fichier JSON propre (sans les états UI/navigation).

Usage :
    python export_json.py <fichier.vaudtax> [sortie.json]
    python export_json.py <fichier.vaudtax> [sortie.json] --full
    # Si le chemin de sortie est omis, écrit dans <nom>.json

Les identifiants directs (NAVS13, IBAN, téléphone, e-mail) sont masqués par
défaut ; --full les exporte en clair.
"""

import argparse
import json
from pathlib import Path
from parse_vaudtax import open_vaudtax, summarize, redact_identifiers

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Exporte un fichier .vaudtax vers un JSON propre")
    ap.add_argument("file", help="fichier .vaudtax")
    ap.add_argument("output", nargs="?", help="fichier JSON de sortie (défaut : <nom>.json)")
    ap.add_argument("--full", action="store_true",
                    help="exporte les identifiants en clair (NAVS13, IBAN, téléphone, e-mail) ; "
                         "masqués par défaut")
    args = ap.parse_args()

    vaudtax_path = Path(args.file)
    output_path = Path(args.output) if args.output else vaudtax_path.with_suffix(".json")

    root, _ = open_vaudtax(vaudtax_path)
    data = summarize(root)
    if not args.full:
        redact_identifiers(data)

    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"Exporté dans {output_path}")
