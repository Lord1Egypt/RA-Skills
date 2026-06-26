#!/usr/bin/env python3
"""
Extraction DÉTERMINISTE des champs d'un document comptable.

Usage :
  python3 extract.py <fichier.pdf>

Sortie : un objet JSON sur stdout. Champs introuvables → null.
L'appelant ne devine JAMAIS : si un champ obligatoire est null,
il classe en needs_review (et n'invente ni montant ni numéro).

  invoice :
    {"kind":"invoice","invoice_id","issue_date","due_date",
     "total_ht","tva_rate","tva_amount","total_ttc",
     "emitter","recipient","siren_found":[...]}

  bank-statement :
    {"kind":"bank-statement","holder","iban","bank",
     "period_start","period_end","opening_balance","closing_balance",
     "operations":[{"date","label","amount","invoice_ref"}]}

  autre : {"kind":"other"}
"""

import json
import re
import subprocess
import sys

BANKS = ["BNP PARIBAS", "CRÉDIT AGRICOLE", "CREDIT AGRICOLE", "SOCIÉTÉ GÉNÉRALE",
         "SOCIETE GENERALE", "LA BANQUE POSTALE", "CIC", "LCL", "HSBC",
         "CAISSE D'ÉPARGNE", "CAISSE D'EPARGNE", "BANQUE POPULAIRE"]
BANK_TOKENS = ("BNP", "AGRICOLE", "GÉNÉRALE", "GENERALE", "POSTALE", "CIC",
               "LCL", "HSBC", "ÉPARGNE", "EPARGNE", "POPULAIRE")

INVOICE_ID_RE = re.compile(
    r"\b([A-Z]{1,4}\d{0,3}-\d{2,4}-\d{2,8}|[A-Z]{2,4}\d{4,12}|\d{4}-\d{2,8})\b")


# ── Helpers ───────────────────────────────────────────────────────────────

def pdftext(path):
    try:
        r = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                           capture_output=True, text=True, errors="ignore", timeout=30)
        return r.stdout
    except Exception:
        return ""


def parse_money(s):
    s = s.replace("\xa0", " ")
    m = re.search(r"\d[\d \.]*,\d{2}|\d[\d \.]+|\d+", s)
    if not m:
        return None
    v = m.group(0).replace(" ", "")
    if "," in v:
        v = v.replace(".", "").replace(",", ".")
    try:
        return round(float(v), 2)
    except ValueError:
        return None


def amount_after(label_re, text):
    """Premier montant trouvé sur une ligne contenant le label."""
    for line in text.splitlines():
        if re.search(label_re, line, re.IGNORECASE):
            chunks = re.findall(r"[\d\xa0 ]+,\d{2}", line.replace("\xa0", " "))
            if chunks:
                return parse_money(chunks[-1])
    return None


def iso_date(dd_mm_yyyy):
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", dd_mm_yyyy)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None


def date_after(label_re, text):
    for line in text.splitlines():
        if re.search(label_re, line, re.IGNORECASE):
            m = re.search(r"\d{2}/\d{2}/\d{4}", line)
            if m:
                return iso_date(m.group(0))
    return None


def first_date(text):
    m = re.search(r"\b\d{2}/\d{2}/\d{4}\b", text)
    return iso_date(m.group(0)) if m else None


def extract_invoice_ref(label):
    m = re.search(r"\b(?:REF|FACT|FACTURE)\s+([A-Za-z0-9][\w\-/]+)", label, re.IGNORECASE)
    return m.group(1) if m else None


def siren_list(text):
    return re.findall(r"\b\d{3}\s?\d{3}\s?\d{3}\b", text)


# ── Classification ────────────────────────────────────────────────────────

def looks_like_statement(t):
    up = t.upper()
    if "RELEVÉ DE COMPTE" in up or "RELEVE DE COMPTE" in up or "ACCOUNT STATEMENT" in up:
        return True
    if "RELEVÉ BANCAIRE" in up or "EXTRAIT DE COMPTE" in up:
        return True
    if "SOLDE D'OUVERTURE" in up or "SOLDE D'OUVERTURE" in up or "SOLDE DE CLÔTURE" in up or "SOLDE DE CLOTURE" in up:
        return True
    if any(b in up for b in BANKS) and ("RELEVÉ" in up or "RELEVE" in up):
        return True
    return False


def has_invoice_guard(t):
    up = t.upper()
    return ((("FACTURE" in up) or ("INVOICE" in up) or ("BON DE FACTURATION" in up))
            and (("SIRET" in up) or ("TVA" in up)))


def looks_like_invoice(t):
    up = t.upper()
    score = 0
    if "FACTURE" in up or "INVOICE" in up or "BON DE FACTURATION" in up or "BILL" in up:
        score += 1
    if "SIRET" in up or re.search(r"N°?\s*TVA", up) or "SIREN" in up:
        score += 1
    if "FACTURÉ À" in up or "FACTURE A" in up or "DESTINATAIRE" in up or "BILL TO" in up or "\nCLIENT" in up:
        score += 1
    if "TOTAL TTC" in up or "NET À PAYER" in up or "TOTAL HT" in up or "NET A PAYER" in up:
        score += 1
    return score >= 2


# ── Extraction facture ────────────────────────────────────────────────────

def company_before_siret(text):
    """Première ligne « réelle » = nom du vendeur (avant le 1er SIRET)."""
    seen_lines = text.splitlines()
    for l in seen_lines[:15]:
        chunk = re.split(r"\s{2,}", l.strip())[0].strip().strip(":")
        if not chunk or len(chunk) < 3:
            continue
        if re.match(r"(FACTURE|INVOICE|BON DE FACTURATION)\b", chunk, re.I):
            continue
        if re.search(r"^\d", chunk):
            continue
        if not re.search(r"[A-Za-zÀ-ÿ]{3,}", chunk):
            continue
        return chunk
    return None


def recipient_block(text):
    lines = text.splitlines()
    label_re = re.compile(r"FACTUR[ÉE]\s*[ÀA]\b|DESTINATAIRE\b|BILL\s*TO\b|^\s*CLIENT\b", re.I)
    for i, l in enumerate(lines):
        if not label_re.search(l):
            continue
        after = label_re.split(l)[-1].strip().lstrip(":").strip()
        candidates = ([after] if after else []) + [lines[j].strip() for j in range(i + 1, min(i + 5, len(lines)))]
        for c in candidates:
            parts = [p.strip() for p in re.split(r"\s{2,}", c) if p.strip()]
            for p in reversed(parts):  # le destinataire est dans la colonne de droite
                if len(p) < 3:
                    continue
                if re.match(r"(ÉCHÉANCE|ECHEANCE|SIRET|N°|TVA|RÈGLEMENT|REGLEMENT)\b", p, re.I):
                    continue
                if re.match(r"^[\d\s/.,€-]+$", p):
                    continue
                if re.search(r"[A-Za-zÀ-ÿ]{3,}", p):
                    return p
    return None


def extract_invoice(text):
    inv_id = None
    # Ordre des patterns : du plus strict (forme structurée) au plus large.
    # Critique : « FACTURE … N° X » avec N° optionnel matchait à tort le N de
    # « Numérix » (sur la ligne d'après FACTURE), d'où la capture « umérix »
    # observée en prod. → On exige `N°` strict et un id structuré en tête.
    for pat in (
        # 1) Forme structurée standard : "N° F1-2026-0001", "N° R3-2026-0003"
        r"\bN\s*[°O]\s*([A-Z]{1,4}\d{0,3}[\-/]\d{2,4}[\-/]\d{2,8})\b",
        # 2) "FACTURE … N° X" avec X structuré (filet pour layouts exotiques)
        r"\bFACTURE\b[\s\S]{0,200}?\bN\s*[°O]\s*([A-Z]{1,4}\d{0,3}[\-/]\d{2,4}[\-/]\d{2,8})\b",
        # 3) "Facture : X" / "Facture # X" — séparateur explicite
        r"\bFACTURE\s*[:#]\s*([A-Za-z0-9][\w\-/]{2,})",
        # 4) "Réf. facture : X"
        r"\bR[ÉE]F\.?\s*FACTURE\s*[:\-]?\s*([A-Za-z0-9][\w\-/]{2,})",
        # 5) Filet de sécurité : "N° X" forme compacte sans tirets
        r"\bN\s*[°O]\s*([A-Z]{2,4}\d{4,12})\b",
    ):
        m = re.search(pat, text, re.I)
        if m:
            inv_id = m.group(1).strip().strip(".:,")
            break
    if not inv_id:
        m = INVOICE_ID_RE.search(text)
        if m:
            inv_id = m.group(1)
    if inv_id and (inv_id.upper() in ("TVA", "SIRET", "HT", "TTC", "FR") or len(inv_id) < 3
                   or re.match(r"^\d{1,3}$", inv_id)):
        inv_id = None

    total_ttc = amount_after(r"NET\s*[ÀA]\s*PAYER|TOTAL\s*TTC|MONTANT\s*TTC", text)
    total_ht = amount_after(r"TOTAL\s*HT|SOUS-?TOTAL\s*HT|MONTANT\s*HT|TOTAL\s*H\.?T\.?", text)
    tva_amount = amount_after(r"(?<!N°\s)(?<!N° )\bTVA\b(?!\s*INTRA)", text)

    tva_rate = None
    mr = re.search(r"TVA\s*\(?\s*([\d,\.]+)\s*%", text, re.I)
    if mr:
        try:
            tva_rate = round(float(mr.group(1).replace(",", ".")) / 100, 4)
        except ValueError:
            pass
    up = text.upper()
    if tva_rate is None and ("TVA NON APPLICABLE" in up or "EXONÉR" in up or "EXONER" in up
                             or "ART. 261" in up or "ART 261" in up):
        tva_rate = 0.0
        if tva_amount is None:
            tva_amount = 0.0

    return {
        "kind": "invoice",
        "invoice_id": inv_id,
        "issue_date": date_after(r"\bDATE\b\s*:", text) or date_after(r"\bDATE\b", text) or first_date(text),
        "due_date": date_after(r"ÉCHÉANCE|ECHEANCE|[ÀA]\s*RÉGLER\s*AVANT|[ÀA]\s*REGLER\s*AVANT", text),
        "total_ht": total_ht,
        "tva_rate": tva_rate,
        "tva_amount": tva_amount,
        "total_ttc": total_ttc,
        "emitter": company_before_siret(text),
        "recipient": recipient_block(text),
        "siren_found": siren_list(text),
    }


# ── Extraction relevé bancaire ────────────────────────────────────────────

def extract_statement(text):
    up = text.upper()
    bank = next((b for b in BANKS if b in up), None)

    m = re.search(r"IBAN\s*:?\s*([A-Z]{2}[A-Z0-9 ]{10,32})", text)
    iban = m.group(1).strip() if m else None

    period_start = period_end = None
    mp = re.search(r"P[ÉE]RIODE\s*:?\s*(\d{2}/\d{2}/\d{4})\s*[—\-–à]+\s*(\d{2}/\d{2}/\d{4})", text, re.I)
    if mp:
        period_start, period_end = iso_date(mp.group(1)), iso_date(mp.group(2))

    opening = amount_after(r"SOLDE\s*D[''’]?\s*OUVERTURE|ANCIEN\s*SOLDE", text)
    closing = amount_after(r"SOLDE\s*DE\s*CL[ÔO]TURE|NOUVEAU\s*SOLDE|SOLDE\s*FINAL", text)

    HEADER_KW = re.compile(
        r"^(RELEV|EXTRAIT|COMPTE|IBAN|BIC|PÉRIODE|PERIODE|SOLDE|ANCIEN\s|NOUVEAU\s|"
        r"DATE|VALEUR|LIBELL|MONTANT|OP[ÉE]RATION|D[ÉE]BIT|CR[ÉE]DIT|TITULAIRE|ÉDIT|EDIT|PAGE)\b")
    holder = None
    fallback = None
    for l in text.splitlines()[:16]:
        for p in [x.strip() for x in re.split(r"\s{2,}", l) if x.strip()]:
            if len(p) < 4 or not re.search(r"[A-Za-zÀ-ÿ]{3,}", p):
                continue
            pu = p.upper()
            if HEADER_KW.match(pu):
                continue
            if pu in (b.upper() for b in BANKS) or any(tok in pu for tok in BANK_TOKENS):
                continue
            # un nom d'entreprise contient en général des minuscules ;
            # les en-têtes/banques sont en capitales
            if re.search(r"[a-zà-ÿ]", p):
                holder = p
                break
            if fallback is None:
                fallback = p
        if holder:
            break
    holder = holder or fallback

    operations = []
    for line in text.splitlines():
        m = re.match(
            r"\s*(\d{2}/\d{2}/\d{4})\s{2,}(.+?)\s{2,}([\d\xa0 ]+,\d{2})\s*€?\s*(CR|DB|CRÉDIT|DÉBIT)?\s*$",
            line.replace("\xa0", " "), re.I)
        if not m:
            continue
        amt = parse_money(m.group(3))
        if amt is None:
            continue
        flag = (m.group(4) or "").upper()
        if flag.startswith("DB") or flag.startswith("DÉB") or flag.startswith("DEB"):
            amt = -amt
        label = m.group(2).strip()
        operations.append({
            "date": iso_date(m.group(1)),
            "label": label,
            "amount": amt,
            "invoice_ref": extract_invoice_ref(label),
        })

    return {
        "kind": "bank-statement",
        "holder": holder,
        "iban": iban,
        "bank": bank,
        "period_start": period_start,
        "period_end": period_end,
        "opening_balance": opening,
        "closing_balance": closing,
        "operations": operations,
    }


# ── Main ──────────────────────────────────────────────────────────────────

def classify_and_extract(text):
    if not text.strip():
        return {"kind": "other", "error": "no text extracted"}
    if looks_like_statement(text) and not has_invoice_guard(text):
        return extract_statement(text)
    if looks_like_invoice(text):
        return extract_invoice(text)
    if looks_like_statement(text):
        return extract_statement(text)
    return {"kind": "other"}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"kind": "other", "error": "usage: extract.py <pdf>"}))
        return
    out = classify_and_extract(pdftext(sys.argv[1]))
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
