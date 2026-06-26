#!/usr/bin/env python3
"""
Moteur du skill `rapprochement-bancaire`.

Travaille sur l'arborescence `clients/<slug>/...` produite par `organisation-documents` (scripts/main.py).
Toute l'extraction de texte est déléguée à `extract.py` (source unique).

Pour chaque période active :
  - lit les factures (nom de fichier conventionnel, sinon contenu PDF via extract.py)
  - lit les relevés bancaires (transactions ligne par ligne via extract.py)
  - rapproche chaque facture avec son paiement (Pass 1 = réf facture, Pass 2 = fuzzy)
  - valide la TVA de chaque facture
  - détecte les anomalies (doublon, facture manquante, orphelin, TVA, retard)
  - écrit followup.json / relances.json / anomalies.json par client
  - produit un rapport consolidé

Usage :
  python3 main.py [<racine_clients>]
  <racine_clients> par défaut : ./clients
"""

import json
import re
import sys
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("clients")
TODAY = datetime.utcnow().date()
ACTIVE_MONTHS = {
    TODAY.strftime("%Y-%m"),
    (TODAY.replace(day=1) - timedelta(days=1)).strftime("%Y-%m"),
}


# ── IO ────────────────────────────────────────────────────────────────────

def load_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def pdf_fields(pdf_path):
    return extract.classify_and_extract(extract.pdftext(pdf_path))


# ── Helpers ───────────────────────────────────────────────────────────────

def parse_invoice_filename(filename):
    """
    Format conventionnel (écrit par organisation-documents/scripts/main.py) :
      AAAA-MM-JJ_N°Facture_Contrepartie_MontantTTC.pdf
    Tolère aussi un ancien format 3 parties (sans n° de facture).
    """
    m = re.match(r"(\d{4}-\d{2}-\d{2})_([^_]+)_([^_]+)_(\d+(?:\.\d+)?)\.pdf$", filename)
    if m:
        issued = m.group(1)
        return {
            "invoice_id": m.group(2),
            "issued_date": issued,
            "due_date": (datetime.strptime(issued, "%Y-%m-%d") + timedelta(days=30)).strftime("%Y-%m-%d"),
            "counterparty": m.group(3),
            "amount": float(m.group(4)),
        }
    m = re.match(r"(\d{4}-\d{2}-\d{2})_([^_]+)_(\d+(?:[._]\d+)?)\.pdf$", filename)
    if m:
        issued = m.group(1)
        amount_raw = m.group(3).replace("_", ".")
        return {
            "invoice_id": f"{issued}_{m.group(2)}_{amount_raw}",
            "issued_date": issued,
            "due_date": (datetime.strptime(issued, "%Y-%m-%d") + timedelta(days=30)).strftime("%Y-%m-%d"),
            "counterparty": m.group(2),
            "amount": float(amount_raw),
        }
    return None


def similarity(a, b):
    a, b = (a or "").lower().strip(), (b or "").lower().strip()
    if not a or not b:
        return 0.0
    if a == b or a in b or b in a:
        return 1.0
    # forme normalisée : hyphens/ponctuation → espace (gère noms tronqués type "Auberge-du-Vie")
    a_clean = re.sub(r"[^a-z0-9]+", " ", a).strip()
    b_clean = re.sub(r"[^a-z0-9]+", " ", b).strip()
    if a_clean and b_clean and (a_clean in b_clean or b_clean in a_clean):
        return 0.9
    base = SequenceMatcher(None, a, b).ratio()
    wa, wb = set(re.findall(r"[a-z0-9]+", a)), set(re.findall(r"[a-z0-9]+", b))
    jacc = len(wa & wb) / len(wa | wb) if (wa and wb) else 0.0
    return max(base, jacc)


def is_locked(month_dir):
    return (month_dir / "batch.lock.json").exists()


def should_process(month_dir):
    key = f"{month_dir.parent.name}-{month_dir.name}"
    return key in ACTIVE_MONTHS or not is_locked(month_dir)


def check_tva(fields):
    ht = fields.get("total_ht")
    rate = fields.get("tva_rate")
    declared = fields.get("tva_amount")
    if ht is None or rate is None or declared is None:
        return None
    if rate == 0:
        return None
    expected = round(ht * rate, 2)
    if expected == 0:
        return None
    disc = abs(declared - expected) / expected
    if disc > 0.05:
        return {
            "type": "tva_incorrecte",
            "total_ht": ht, "tva_declared": declared, "tva_expected": expected,
            "tva_rate_pct": round(rate * 100, 1), "discrepancy_pct": round(disc * 100, 1),
            "blocking": True,
        }
    return None


# ── Traitement d'un client ────────────────────────────────────────────────

def process_client(client_dir):
    invoices = {}
    transactions = []
    anomalies = []

    for year_dir in sorted(client_dir.iterdir()):
        if not (year_dir.is_dir() and re.match(r"\d{4}$", year_dir.name)):
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir() or not should_process(month_dir):
                continue

            # ── Factures ──────────────────────────────────────────────────
            for f in month_dir.rglob("invoices/**/*.pdf"):
                direction = "out" if "/out/" in str(f).replace("\\", "/") else "in"
                parsed = parse_invoice_filename(f.name)
                fields = pdf_fields(f)

                if parsed:
                    inv_id = parsed["invoice_id"]
                    amount = parsed["amount"]
                    issued = parsed["issued_date"]
                    due = parsed["due_date"]
                    cp = parsed["counterparty"]
                elif fields.get("kind") == "invoice" and fields.get("invoice_id") and fields.get("total_ttc") is not None:
                    inv_id = fields["invoice_id"]
                    amount = fields["total_ttc"]
                    issued = fields.get("issue_date") or ""
                    due = ((datetime.strptime(issued, "%Y-%m-%d") + timedelta(days=30)).strftime("%Y-%m-%d")
                           if issued else (TODAY + timedelta(days=30)).strftime("%Y-%m-%d"))
                    cp = (fields.get("recipient") if direction == "out" else fields.get("emitter")) or client_dir.name
                else:
                    anomalies.append({"type": "facture_illisible", "source_file": str(f), "blocking": False})
                    continue

                # nom complet de la contrepartie pour le matching fuzzy ;
                # si extract.py a su lire le PDF, on récupère le numéro réel — ça permet
                # de rattraper un nom de fichier corrompu en amont (invoice_id incorrect).
                cp_name = (fields.get("recipient") if direction == "out" else fields.get("emitter")) or cp
                real_inv_id = fields.get("invoice_id") if fields.get("kind") == "invoice" else None
                if real_inv_id and real_inv_id != inv_id:
                    inv_id = real_inv_id  # le PDF a raison, le filename a tort

                # clé interne = chemin (unique) — l'invoice_id peut collisionner si l'amont
                # a mal nommé plusieurs fichiers à l'identique.
                invoices[str(f)] = {
                    "invoice_id": inv_id, "type": direction, "amount": amount,
                    "status": "unpaid", "issued_date": issued, "due_date": due,
                    "counterparty": cp, "counterparty_name": cp_name,
                    "bank_matched": False, "source_file": str(f),
                }

                if fields.get("kind") == "invoice":
                    tva_anom = check_tva(fields)
                    if tva_anom:
                        tva_anom["invoice_id"] = inv_id
                        anomalies.append(tva_anom)

            # ── Relevés bancaires ─────────────────────────────────────────
            for st in month_dir.rglob("bank-statements/*"):
                if not st.is_file():
                    continue
                f = pdf_fields(st)
                ops = f.get("operations", []) if f.get("kind") == "bank-statement" else []
                for op in ops:
                    transactions.append({
                        "date": op.get("date"),
                        "label": (op.get("label") or "").lower(),
                        "raw_label": op.get("label") or "",
                        "amount": op.get("amount"),
                        "invoice_ref": op.get("invoice_ref"),
                    })
                if not ops:
                    anomalies.append({"type": "releve_non_parseable", "source_file": str(st), "blocking": False})

    # ── Rapprochement (montant comparé en valeur absolue) ─────────────────
    # Pass 1 — réf facture présente dans le libellé bancaire (REF/FACT <id>)
    for inv in invoices.values():
        for tx in transactions:
            if tx.get("invoice_ref") and tx["invoice_ref"] == inv["invoice_id"]:
                paid = round(abs(tx["amount"]), 2)
                if abs(paid - inv["amount"]) <= 1.0:
                    inv["status"] = "paid"
                elif paid < inv["amount"]:
                    inv["status"] = "partial"
                    inv["amount_paid"] = paid
                    inv["amount_remaining"] = round(inv["amount"] - paid, 2)
                else:
                    inv["status"] = "paid"
                    inv["amount_paid"] = paid
                    inv["overpaid_by"] = round(paid - inv["amount"], 2)
                inv["bank_matched"] = True
                inv["matched_tx"] = tx["raw_label"]
                break

    # Pass 2 — fuzzy : |montant| ±1€ + similarité libellé / contrepartie ≥ 0.6
    for inv in invoices.values():
        if inv["bank_matched"]:
            continue
        for tx in transactions:
            if abs(abs(tx["amount"]) - inv["amount"]) > 1.0:
                continue
            if similarity(tx["label"], inv.get("counterparty_name", "")) >= 0.6:
                inv["status"] = "paid"
                inv["bank_matched"] = True
                inv["matched_tx"] = tx["raw_label"]
                break

    # ── Anomalies ─────────────────────────────────────────────────────────
    # Doublons de paiement (même date + montant + libellé)
    seen = {}
    for tx in transactions:
        key = (tx["date"], round(abs(tx["amount"]), 2), tx["label"][:30])
        if key in seen:
            anomalies.append({"type": "doublon_paiement", "label": tx["raw_label"],
                              "amount": tx["amount"], "date": tx["date"], "blocking": True})
        else:
            seen[key] = True

    # Ligne du relevé qui cite un n° de facture absent du dossier
    known = {inv["invoice_id"] for inv in invoices.values()}
    matched_label_set = {inv.get("matched_tx") for inv in invoices.values() if inv.get("matched_tx")}
    for tx in transactions:
        ref = tx.get("invoice_ref")
        if not ref or ref in known:
            continue
        # Garde-fou : si la transaction a déjà été rapprochée à une facture via Pass 2
        # (montant + nom de contrepartie), la divergence de référence est probablement
        # un nommage de fichier incorrect en amont, pas une vraie facture manquante.
        if tx["raw_label"] in matched_label_set:
            continue
        anomalies.append({"type": "facture_manquante", "invoice_ref": ref, "label": tx["raw_label"],
                          "amount": tx["amount"], "date": tx["date"],
                          "blocking": abs(tx["amount"]) > 1000})

    # Encaissements sans aucune référence ni facture
    matched = {inv.get("matched_tx") for inv in invoices.values() if inv.get("matched_tx")}
    for tx in transactions:
        if tx["amount"] is None or tx["amount"] <= 0 or tx["raw_label"] in matched or tx.get("invoice_ref"):
            continue
        anomalies.append({"type": "paiement_orphelin", "label": tx["raw_label"],
                          "amount": tx["amount"], "date": tx["date"], "blocking": tx["amount"] > 1000})

    # ── Statuts overdue + relances ────────────────────────────────────────
    relances = []
    for inv in invoices.values():
        try:
            due = datetime.strptime(inv["due_date"], "%Y-%m-%d").date()
        except (ValueError, KeyError):
            due = TODAY + timedelta(days=30)

        if inv["status"] in ("unpaid",) and due < TODAY:
            inv["status"] = "overdue"
            anomalies.append({"type": "invoice_overdue", "invoice_id": inv["invoice_id"],
                              "days_late": (TODAY - due).days, "amount": inv["amount"], "blocking": False})

        if inv["status"] in ("overdue", "partial") or (inv["status"] == "unpaid" and due < TODAY):
            days_late = max((TODAY - due).days, 0)
            step = 1 if days_late <= 30 else 2 if days_late <= 60 else 3 if days_late <= 90 else "escalation"
            r = {"invoice_id": inv["invoice_id"], "counterparty": inv.get("counterparty", ""),
                 "amount": inv["amount"], "due_date": inv.get("due_date"), "days_late": days_late,
                 "step": step, "status": "pending",
                 "next_action_date": (TODAY + timedelta(days=5)).strftime("%Y-%m-%d")}
            if inv["status"] == "partial":
                r["amount_remaining"] = inv.get("amount_remaining", inv["amount"])
                r["note"] = f"Solde restant dû : {r['amount_remaining']:.2f} €"
            relances.append(r)

    save_json(client_dir / "followup.json", list(invoices.values()))
    save_json(client_dir / "relances.json", relances)
    save_json(client_dir / "anomalies.json", anomalies)
    return invoices, relances, anomalies


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    if not ROOT.exists():
        print(f"✗ Racine introuvable : {ROOT}")
        sys.exit(1)

    report = {"date": TODAY.isoformat(), "clients": []}
    tot_inv = tot_paid = tot_rel = tot_anom = tot_block = 0

    for client_dir in sorted(ROOT.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith("_"):
            continue
        invoices, relances, anomalies = process_client(client_dir)
        paid = sum(1 for i in invoices.values() if i["status"] == "paid")
        block = sum(1 for a in anomalies if a.get("blocking"))
        report["clients"].append({
            "client": client_dir.name, "invoices": len(invoices), "paid": paid,
            "matched": sum(1 for i in invoices.values() if i.get("bank_matched")),
            "relances": len(relances), "anomalies": len(anomalies), "blocking_anomalies": block,
        })
        tot_inv += len(invoices); tot_paid += paid; tot_rel += len(relances)
        tot_anom += len(anomalies); tot_block += block

    report["totals"] = {"invoices": tot_inv, "rapprochements": tot_paid,
                        "relances": tot_rel, "anomalies": tot_anom, "blocking_anomalies": tot_block}
    save_json(Path(f"compta_batch_report_{TODAY}.json"), report)
    print(f"✓ {len(report['clients'])} clients — {tot_paid}/{tot_inv} rapprochés — "
          f"{tot_rel} relances — {tot_anom} anomalies ({tot_block} bloquantes)")
    for c in report["clients"]:
        print(f"  · {c['client']}: {c['paid']}/{c['invoices']} payées, {c['relances']} relances, {c['anomalies']} anomalies")
    print(f"  Rapport : compta_batch_report_{TODAY}.json")


if __name__ == "__main__":
    main()
