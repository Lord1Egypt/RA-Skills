# Multi-Agent Orchestration System

## Purpose

The orchestration system coordinates the universal operator skills so they behave like a focused executive team instead of disconnected assistants.

## Default Routing Logic

| User Request Type | Primary Operator | Supporting Operators |
|---|---|---|
| Company direction, priorities, positioning | CEO / Strategy | Data, Finance, Growth |
| Product build, feature planning, tech stack | Product / Engineering | Design, Data, Legal |
| User acquisition, content, launch, funnel | Growth / Marketing | Design, Data, Community |
| Revenue, outreach, integrations, deals | Sales / Partnerships | Finance, Legal, CEO |
| Internal systems, SOPs, accountability | Operations / COO | CEO, Data, Customer Success |
| Budget, pricing, runway, profitability | Finance | CEO, Sales, Data |
| Support, onboarding, retention, feedback | Customer Success | Product, Data, Community |
| Metrics, dashboards, experiments | Data / Analytics | CEO, Growth, Product |
| Interface, customer journey, brand experience | Design / UX | Product, Growth, Customer Success |
| Legal, compliance, contracts, policies | Legal / Compliance | CEO, Finance, Sales |
| Audience, Discord, events, engagement | Community | Growth, Customer Success, Product |
| Overnight / async work, morning brief, founder brief | Night Shift | Any operator(s) the objective routes into |

## Orchestration Flow

1. Intake the business context.
2. Classify the request by objective.
3. Select one primary operator.
4. Add supporting operators only when their role materially improves the result.
5. Assign each operator a clear deliverable.
6. Merge outputs into one final plan.
7. Identify conflicts, risks, and open questions.
8. Produce prioritized next actions.

## Example Prompts

### Broad Request
"Analyze this business and tell me what team roles need to take over."

Use:
- universal_business_operator
- universal_ceo_operator
- universal_operations_coo_operator

### Launch Request
"Create a launch plan for this new product."

Use:
- universal_business_operator
- universal_growth_marketing_operator
- universal_product_engineering_operator
- universal_sales_partnerships_operator
- universal_customer_success_operator

### Revenue Request
"Help me turn this project into a profitable business."

Use:
- universal_ceo_operator
- universal_finance_operator
- universal_sales_partnerships_operator
- universal_growth_marketing_operator

## Anti-Overlap Rule

Each operator must own a separate lane. If two operators produce conflicting recommendations, the CEO / Strategy Operator resolves the tradeoff.

## Night Shift Routing

The Night Shift Operator (`universal_night_shift_operator`) is the execution layer for overnight / asynchronous work. It does not own a domain lane — instead, it classifies the user's objective, splits it into work packets, and routes each packet to the correct existing operator from the table above.

### Trigger Commands

| Command | Routes To | Output |
|---|---|---|
| `/run nightshift [objective]` | `universal_night_shift_operator` | Morning Brief |
| `/run overnight [objective]` | `universal_night_shift_operator` (alias) | Morning Brief |
| `/run morning-brief [objective]` | `universal_night_shift_operator` (alias) | Morning Brief |
| `/run founder-brief [objective]` | `universal_night_shift_operator` (alias) | Morning Brief |

### Night Shift Orchestration Flow

1. Receive a nightshift / overnight / morning-brief / founder-brief command.
2. Activate `universal_night_shift_operator`.
3. The night shift operator classifies the objective into one or more domains.
4. It splits the objective into 3-8 work packets (see `NIGHT_SHIFT.md` for the packet schema).
5. It safety-checks every packet against `SAFETY_RULES.md` (PASS / DRAFT-ONLY / BLOCKED).
6. It routes each packet to the correct universal operator using the routing table above.
7. Each routed operator produces only deliverables — never live actions.
8. Conflicts are resolved by `universal_ceo_operator` in the Executive Summary.
9. The night shift operator aggregates everything into a single Morning Brief, following the exact structure in `MORNING_BRIEF.md`.
10. All irreversible or out-of-scope items are flagged under **Decisions Needed** in the brief, not executed.

### Night Shift Example

"`/run overnight prep everything I need to decide tomorrow whether to raise prices`"

Use:
- `universal_night_shift_operator` (coordinator)
- `universal_ceo_operator` (framing memo, final recommendation)
- `universal_finance_operator` (pricing scenarios)
- `universal_customer_success_operator` (churn-risk analysis)
- `universal_sales_partnerships_operator` (sales talk-track draft)
- `universal_growth_marketing_operator` (customer announcement draft)
- `universal_data_analytics_operator` (post-change metric watch spec)

Output: a single Morning Brief. Drafts are marked `DRAFT — NOT SENT` / `DRAFT — NOT PUBLISHED`. The actual pricing change and any external communication remain user-only decisions, listed under **Decisions Needed**.
