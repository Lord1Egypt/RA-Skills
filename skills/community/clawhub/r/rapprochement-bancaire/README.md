# rapprochement-bancaire

> Claude skill for **French accounting firms** (`cabinets comptables`). Reads the `clients/<slug>/...` tree produced by [`organisation-documents`](https://github.com/developers-trendex/organisation-documents), reconciles each invoice with its bank-statement transaction, validates VAT, and writes one `followup.json` / `relances.json` / `anomalies.json` per client plus a consolidated report. Deterministic script-driven.

## What it does

For each invocation, the skill runs **one command** :

```bash
python3 scripts/main.py <clients_root>
```

That script:

1. Walks every client folder under `<clients_root>` (skipping `_a-identifier/`, `_incomplet/`, `_non-attribue/`, `_cabinet/`).
2. For each active period (current + previous month, plus any older month without `batch.lock.json`) :
   - Reads invoices from `invoices/in/` and `invoices/out/`.
   - Reads transactions from `bank-statements/` via `scripts/extract.py` (one line per transaction, with the `REF`/`FACT <id>` reference captured when present).
3. Reconciles in two passes (amount compared in absolute value — an `out` invoice is settled by a credit, an `in` by a debit) :
   - **Pass 1** — direct match by invoice reference (`REF` / `FACT` in the bank label). Exact amount (±1 €) → `paid` ; lower amount → `partial` with `amount_paid` and `amount_remaining` ; higher → `paid` with `overpaid_by`.
   - **Pass 2** — fuzzy : `|amount| ±1 €` **and** counterparty-name similarity ≥ 0.6.
   - No match + due date passed → `overdue`.
4. Validates VAT on each invoice : if `|VAT declared − TOTAL HT × rate| / expected > 5 %`, flags a blocking `tva_incorrecte` anomaly (exempted-VAT invoices are silently ignored).
5. Detects other anomalies (see below).
6. Generates relances based on lateness (`overdue`, `partial`, `unpaid` past due).
7. Writes per-client JSON files + `compta_batch_report_<date>.json` consolidated.

The agent only **reads the JSON files and relays the summary to the accountant** — payments, late invoices, anomalies (highlighting blocking ones), no technical paths.

## Statuses (`followup.json`)

| Status     | Meaning                                                                   |
| ---------- | ------------------------------------------------------------------------- |
| `unpaid`   | Not yet due, no payment                                                   |
| `paid`     | Payment confirmed                                                         |
| `partial`  | Partial payment — `amount_paid` + `amount_remaining` kept                 |
| `overdue`  | Due date passed, no payment                                               |

## Anomalies (`anomalies.json`)

**Blocking** (period cannot be locked) :

| Type                          | Condition                                                                                       |
| ----------------------------- | ----------------------------------------------------------------------------------------------- |
| `doublon_paiement`            | same date + amount + label                                                                      |
| `tva_incorrecte`              | calculated/declared VAT gap > 5 %                                                                |
| `facture_manquante`           | a bank line references an invoice number (`REF`/`FACT`) absent from the folder, amount > 1 000 €|
| `paiement_orphelin`           | credit > 1 000 € with no reference and no matching invoice                                       |

**Non-blocking** (signaled, period can still be locked) :

| Type                          | Condition                                                                                       |
| ----------------------------- | ----------------------------------------------------------------------------------------------- |
| `facture_manquante`           | as above, amount ≤ 1 000 €                                                                      |
| `paiement_orphelin`           | credit ≤ 1 000 € with no reference                                                              |
| `releve_non_parseable`        | no transaction extractable from a statement PDF                                                  |
| `facture_illisible`           | neither filename nor PDF content yield a number + amount                                         |
| `invoice_overdue`             | unpaid past due date                                                                            |

> `facture_manquante` ≠ `paiement_orphelin` : the former is a payment that **cites** an invoice number we never received (client forgot to send it) ; the latter is a credit with no reference at all.

## Relances (`relances.json`)

| Lateness                | Step          |
| ----------------------- | ------------- |
| ≤ 30 days               | 1             |
| ≤ 60 days               | 2             |
| ≤ 90 days               | 3             |
| > 90 days               | `escalation`  |

A `partial` invoice gets a relance with explicit `Solde restant dû : X,XX €`.

## Period closing

A period is locked (`batch.lock.json`) when : no blocking anomaly, file hashes stable for 7 days, no unjustified `unpaid` / `overdue`. Locked periods are never reprocessed unless a file hash changes.

## Prerequisite

The script calls `pdftotext` (package `poppler-utils`). Install it once on the runtime :

```bash
apt install poppler-utils
```

## Output files

```
clients/<slug>/
├── followup.json         ← all invoices with their reconciliation status
├── relances.json         ← invoices needing follow-up, with step + suggested next contact date
├── anomalies.json        ← all anomalies for this client (blocking flag included)
└── <AAAA>/<MM>/batch.lock.json   ← present when the period is closed
```

Plus a consolidated `compta_batch_report_<YYYY-MM-DD>.json` at the workspace root.

## Companion skill

[`organisation-documents`](https://github.com/developers-trendex/organisation-documents) — receives, identifies the firm's clients, and classifies documents into the tree this skill consumes.

## Files

| File                              | Purpose                                                                |
| --------------------------------- | ---------------------------------------------------------------------- |
| `SKILL.md`                        | Skill definition (French) — the "when and how to relay" layer          |
| `scripts/main.py`                 | Entrypoint — reconciliation, anomalies, relances, report               |
| `scripts/extract.py`              | Deterministic extractor (only place that touches `pdftotext`)          |
| `references/matching-rules.md`    | Reference — matching cascade, normalization, edge cases                |
| `references/structure-cible.md`   | Path / naming contract (duplicated from `organisation-documents`)      |

## License

Internal — OpenClaw private use.
