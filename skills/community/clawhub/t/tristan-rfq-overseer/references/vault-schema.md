# Vault Schema

Tristan expects the Obsidian vault to be organized as follows. Paths are
relative to the vault root passed to `obsidian-cli`.

```
<vault-root>/
├── RFQs/
│   └── RFQ-YYYY-NNNN.md          # one note per RFQ, from rfq-note-template.md
├── Certs/
│   └── <Supplier>-<CertType>.md  # one note per certificate, from cert-note-template.md
└── Quotes/
    └── RFQ-YYYY-NNNN/
        └── <supplier>.json       # raw supplier quote, input to compare_quotes.py
```

## RFQ Note Frontmatter

| Field | Type | Notes |
|---|---|---|
| `rfq_id` | string | Format `RFQ-YYYY-NNNN`, sequential per year |
| `status` | string | `intake` → `pricing` → `quoted` → `sent` → `closed` |
| `client` | string | Client/company name |
| `contact_name` | string | Primary contact |
| `contact_email` | string | Primary contact email |
| `source` | string | `email` or `telegram` |
| `due_date` | date | `YYYY-MM-DD` |
| `value_estimate` | number | Rough estimate, refined once pricing runs |
| `created` | date | Note creation date |
| `last_updated` | date | Bumped on every status change |

## Certificate Note Frontmatter

| Field | Type | Notes |
|---|---|---|
| `cert_id` | string | Internal identifier |
| `supplier` | string | Supplier name, must match `Quotes/<supplier>.json` naming |
| `cert_type` | string | e.g. ISO 9001, RoHS, material cert |
| `issue_date` | date | |
| `expiry_date` | date | |
| `status` | string | `valid`, `expiring_soon`, `expired` |
| `linked_rfqs` | list | RFQ IDs this supplier has quoted on |

## Status Transitions

```
intake → pricing → quoted → sent → closed
```

An RFQ note should only move to `sent` after `command.send_draft` has been
confirmed by the user (see `SKILL.md` guardrails). Never set `status: sent`
programmatically before that confirmation is received.
