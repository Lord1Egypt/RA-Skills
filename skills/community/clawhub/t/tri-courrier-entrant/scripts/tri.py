#!/usr/bin/env python3
"""
Étape ① du pipeline comptable — TRI DU COURRIER ENTRANT.

Action humaine : ouvrir un mail et décider en un coup d'œil s'il concerne la
comptabilité, puis en sortir les pièces à traiter et les informations d'en-tête
(expéditeur, domaine, objet) qui serviront plus tard à reconnaître le client.

N'analyse PAS le contenu des pièces (c'est analyse-piece-comptable) et ne range
rien. Décision + normalisation, point.

Usage :
  echo '<mail.json>' | python3 tri.py
  python3 tri.py <mail.json>

Entrée (JSON) :
  {
    "from": "compta@orange-pro.fr",
    "subject": "Facture F-2026-04-1287",
    "body": "Bonjour, veuillez trouver ci-joint…",
    "date": "2026-04-15T09:12:00Z",
    "messageId": "<abc@gmail>",
    "attachments": [
      {"filename": "facture.pdf", "path": "/.../staging/abc.pdf", "mimeType": "application/pdf"}
    ]
  }

Sortie (JSON) : un "dossier" initial, enrichi ensuite par les étapes suivantes.
  {
    "relevant": true,
    "reason": "pièce PDF + mot-clé « facture »",
    "email": {"from","domain","subject","date","messageId"},
    "pieces": [{"filename","path","mimeType"}],
    "ignored_attachments": [{"filename","reason"}]
  }
"""

import json
import re
import sys

# Mots-clés comptables (mêmes repères que le reste du domaine).
KEYWORDS = ("facture", "invoice", "reçu", "recu", "paiement", "payment", "tva",
            "vat", "relevé", "releve", "statement", "acompte", "avoir",
            "net à payer", "total ttc", "bon de facturation")

# Extensions d'une pièce comptable potentielle.
DOC_EXT = (".pdf", ".jpg", ".jpeg", ".png", ".heic", ".tiff", ".tif",
           ".eml", ".xml", ".csv", ".ofx")


def domain_of(addr):
    m = re.search(r"@([^>\s]+)", addr or "")
    return m.group(1).lower() if m else None


def has_keyword(text):
    t = (text or "").lower()
    return next((k for k in KEYWORDS if k in t), None)


def run(mail):
    pieces, ignored = [], []
    for a in mail.get("attachments") or []:
        name = (a.get("filename") or "").lower()
        if name.endswith(DOC_EXT):
            pieces.append({"filename": a.get("filename"),
                           "path": a.get("path"),
                           "mimeType": a.get("mimeType")})
        else:
            ignored.append({"filename": a.get("filename"),
                            "reason": "format non comptable (probablement signature ou image décorative)"})

    kw = has_keyword(mail.get("subject")) or has_keyword(mail.get("body"))

    # Pertinent si une pièce exploitable OU un mot-clé comptable est présent.
    if pieces and kw:
        relevant, reason = True, f"pièce jointe + mot-clé « {kw} »"
    elif pieces:
        relevant, reason = True, "pièce jointe exploitable, à analyser"
    elif kw:
        relevant, reason = True, f"pas de pièce mais mot-clé « {kw} » dans le mail — corps à lire"
    else:
        relevant, reason = False, "aucune pièce comptable ni mot-clé — hors champ comptable"

    return {
        "relevant": relevant,
        "reason": reason,
        "email": {
            "from": mail.get("from"),
            "domain": domain_of(mail.get("from")),
            "subject": mail.get("subject"),
            "date": mail.get("date"),
            "messageId": mail.get("messageId"),
        },
        "pieces": pieces,
        "ignored_attachments": ignored,
    }


def main():
    raw = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1], encoding="utf-8").read()
    try:
        mail = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"entrée JSON invalide : {e}"}))
        sys.exit(1)
    print(json.dumps(run(mail), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
