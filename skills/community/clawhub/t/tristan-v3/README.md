# tristan-rfq-overseer

An OpenClaw/ClawHub skill covering the full RFQ pipeline: intake, draft, pricing, tracking.
Storage is an Obsidian vault. Intake and notifications run over Telegram and email.

* **Codename:** Tristan
* **Wake Phrase:** `"T, we live?"`

---

## Description

Automates the full RFQ pipeline using Obsidian as storage. Handles intake via Telegram/email, pricing with Python scripts, and tracks supplier quotes and certificates.

---

## Directory Structure

````text
tristan-rfq-overseer/
├── SKILL.md                          # The skill itself - triggering + workflow
├── README.md                         # This file (not part of the skill payload)
├── assets/
│   ├── rfq-note-template.md          # Obsidian note template for each RFQ
│   ├── cert-note-template.md         # Obsidian note template for cert tracking
│   └── rfq-response-template.md      # Structural template for drafted responses
├── scripts/
│   ├── pricing_model.py              # Stage 3 pricing calculator
│   └── compare_quotes.py             # Stage 4 supplier quote ranking
└── references/
    ├── vault-schema.md               # Folder structure + frontmatter fields
    ├── telegram-conventions.md       # Intake/reply handling for Telegram
    └── email-conventions.md          # Intake/reply handling for email
````

---

## How to Use

1. **Install dependencies** – `obsidian-cli`, the Telegram channel, and the email channel. Point `obsidian-cli` at your vault.
2. **Drop an RFQ into email** – Forward the RFQ to the connected inbox.
3. **Skill creates the RFQ note in Obsidian** – Using `assets/rfq-note-template.md` with `status: intake`.
4. **Run `pricing_model.py`, optionally `pricing_strategies.py`, and `compare_quotes.py`** – Get the cost-plus baseline, layer on a market/value/target/escalation/TCO comparison if useful, and rank suppliers. Results save to the vault.
5. **Review the draft, confirm, and send via email** – Never sends without explicit confirmation.

> **Note:** Telegram handles internal intake and status updates. Email handles formal external intake and client-side delivery.

---

## Pricing Strategies

Every quote starts from a **cost-plus baseline** (`pricing_model.py`) — this
is the transparency floor and the number every other strategy is compared
against; no strategy is allowed to suggest a price below it.

| Method | Script | Best for |
|---|---|---|
| Cost-plus | `pricing_model.py` | Always run first — the baseline |
| Competitive / market-based | `pricing_strategies.py market` / `report --strategy market` | Positioning against known competitor prices |
| Value-based | `pricing_strategies.py value` | High-value/low-material-cost work |
| Tiered volume | `pricing_strategies.py volume` | Bulk orders with quantity breakpoints |
| Target costing / should-cost | `pricing_strategies.py target` | Checking if a market-driven target price leaves room for margin |
| Index-based / escalation | `pricing_strategies.py escalation` | **Long-term contracts** with a price-adjustment clause |
| Total cost of ownership (TCO) | `pricing_strategies.py tco`, or `compare_quotes.py --tco` | **Long-term/capital purchases** — shows a client the cheapest quote isn't always the cheapest option |

`compare_quotes.py --tco` ranks suppliers by total cost of ownership instead
of sticker price, which is what makes it possible to show a client you're
not just packaging the cheapest quote.

---

### Example RFQ Note Frontmatter

````yaml
rfq_id: RFQ-2026-0042
status: intake
client: Acme Corp
due_date: 2026-05-01
value_estimate: 0
````

---

## Triggers

1. **`wake.phrase`**: `"T, we live?"` → Respond as Tristan and list current RFQ status.
2. **`email.received`**: New email with "RFQ"/"Quotation" → Create note → Telegram alert: `"New RFQ: [ID]"`
3. **`telegram.message`**: Message starts with `/rfq` → Create note → Reply with link.
4. **`command.run_pricing`**: `/price RFQ-0042` → Run `pricing_model.py` → Update note.
5. **`command.compare_quotes`**: `/compare RFQ-0042` → Run `compare_quotes.py` → Stage draft.
6. **`command.send_draft`**: User confirms "yes send" → Send email. **Never auto-send.**

---

## Required ClawHub Dependencies

1. **`obsidian-cli`** – Install via `clawhub install <obsidian-cli-slug>`. Point directly to your active vault.
2. **Telegram channel** – Connected in OpenClaw for intake and push notifications.
3. **Email channel** – AgentMail/Gmail connector for intake and draft delivery.

---

## Publishing to ClawHub

Run the validator before every publish — not just once:

````bash
python3 scripts/validate_package.py .
````

Then publish:

````bash
npm install -g clawhub
clawhub login
clawhub skill publish . --slug tristan-rfq-overseer --name "Tristan RFQ Overseer" --version 1.0.0
````

### Deployment Checklist

* [ ] **Validation:** Run `python3 scripts/validate_package.py .` and confirm it exits clean — every time, not just before the first publish.
* [ ] **Vault Paths:** Ensure the skill points to your real vault location (assumes `RFQs/` and `Certs/` are at root).
* [ ] **Email Guardrail:** Verify that no emails can be sent without manual verification.
* [ ] **Placeholders:** Fill in any outstanding `[NEEDS INPUT:...]` placeholders within the response template.
* [ ] **Testing:** Complete a dry-run test over both Telegram and Email before pushing live.

> **Packaging:** Zip the folder as `tristan-rfq-overseer.zip` keeping the `assets/` directory intact inside, then publish.

---

**ClawHub SUMMARY**: Tristan automates RFQs with Obsidian, Telegram, and email. Pricing + supplier ranking included.
