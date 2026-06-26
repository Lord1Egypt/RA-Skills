# Support Script Library — Output Template

Copy this file and fill it in to produce a finished, hand-off-ready script library. Delete the italic guidance notes once filled.

---

## Library Header

- **Brand:** `{{brand_name}}`
- **Platforms covered:** `{{e.g. Shopify, TikTok Shop, Shopee SG/MY}}`
- **Owner / last reviewer:** `{{name}}`
- **Version / date:** `v{{x.x}} — {{YYYY-MM-DD}}`
- **Voice summary (1-2 lines):** *`{{e.g. "Warm, sensory, lightly playful. First-name basis. One emoji max. Never clinical or legalistic."}}`*
- **Default SLA:** First reply `{{<2h business / <12h off-hours}}`; resolution target `{{e.g. 1 business day}}`.
- **Global do-not-say:** *`{{e.g. never admit fault on injury claims; never quote legal terms; never promise a hard delivery date}}`*

### Variable glossary

*List every placeholder used in the library so agents know what to swap. Add rows as needed.*

| Placeholder | Meaning | Where to find it |
| --- | --- | --- |
| `{{customer_name}}` | Customer first name | Order / chat profile |
| `{{order_id}}` | Order number | Helpdesk / platform order page |
| `{{tracking_link}}` | Live tracking URL | Carrier / fulfilment app |
| `{{eta_date}}` | Realistic delivery / resolution date | Tracking or SLA |
| `{{amount}}` | Refund / credit amount | Order page |
| `{{promo_code}}` | Discount code in question | Promotions list |

---

## Per-Scenario Block (repeat for each scenario)

### Scenario: `{{scenario_name}}`

- **Category:** `{{Order Status / Returns / Product Issue / ...}}`
- **Trigger:** *`{{when an agent reaches for this script — keywords, tags, or situation}}`*
- **Customer emotion:** *`{{e.g. anxious, frustrated, confused}}`*
- **Required info before replying:** *`{{e.g. order ID confirmed, tracking checked, photos received}}`*

**Script — Variant A (standard):**
> `{{paste script with placeholders}}`

**Script — Variant B (high-empathy / repeat or upset customer):**
> `{{paste script with placeholders}}`

**Channel notes:** *`{{e.g. chat = use Variant A short form, drop the sign-off line; email = keep full}}`*

**Escalation path:** *`{{when to hand off and to whom — e.g. "escalate to Tier 2 if value > $X, injury claim, or 3rd contact"}}`*

**Compensation ceiling:** *`{{pre-approved max — e.g. free reship OR 20% credit, whichever lower; manager approval beyond}}`*

**Do-not-say:** *`{{phrasing to avoid for this scenario}}`*

---

*(Duplicate the block above for every scenario in the library. Group blocks under their category headings.)*

---

## Maintenance Log

*Record every change. Review at least monthly.*

| Date | Scenario(s) affected | Change | Reason | Changed by |
| --- | --- | --- | --- | --- |
| `{{YYYY-MM-DD}}` | `{{e.g. "WISMO"}}` | `{{e.g. updated ETA window to 3-5 days}}` | `{{e.g. carrier SLA changed}}` | `{{name}}` |
| | | | | |
| | | | | |

## Review Schedule

- [ ] Monthly: retire unused scripts, add new scenarios from emerging tickets.
- [ ] On any product/price/policy change: audit affected scripts same week.
- [ ] Quarterly: re-run the full quality checklist and refresh the voice summary.
