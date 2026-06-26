# Universal Company Operator System

A project-agnostic OpenClaw-ready operator pack for running or supporting any company, project, product, service, nonprofit, creator brand, or internal initiative.

## Included Skills

- universal_business_operator — master router and multi-agent coordinator
- universal_ceo_operator — strategy and executive decisions
- universal_product_engineering_operator — product, technical planning, and implementation strategy
- universal_growth_marketing_operator — marketing, growth, messaging, and funnels
- universal_sales_partnerships_operator — sales, revenue, partnerships, and distribution
- universal_operations_coo_operator — operations, SOPs, accountability, and execution systems
- universal_finance_operator — budgets, pricing, cash flow, profitability, and financial planning
- universal_customer_success_operator — onboarding, support, retention, and feedback loops
- universal_data_analytics_operator — metrics, dashboards, insights, and optimization
- universal_design_ux_operator — UX, flows, interface clarity, and design systems
- universal_legal_compliance_operator — legal/compliance risk spotting and review frameworks
- universal_community_operator — community building, engagement, moderation, and advocacy
- universal_night_shift_operator — overnight execution coordinator that routes safe, asynchronous work to the other operators and produces a single Morning Brief

## Recommended Usage

Use `universal_business_operator` first when the task is broad or cross-functional. Use individual operators when the request clearly belongs to one function.

## Core Principle

Every operator must understand the project first, then execute its role. No project-specific assumptions are baked in.

## Command-Based Operating System Layer

This package includes an optional command-console operating layer:

- `COMMAND_CONSOLE.md` — command grammar and operator routing
- `OPERATING_SYSTEM.md` — execution cadence, review loops, and operating templates
- `GWAPSPOT_CONTEXT.md` — optional project context for GwapSpot.fun only

Recommended mode: Command Console Mode.

## Night Shift Mode

This package also includes an asynchronous execution layer for overnight or "while-you-sleep" work:

- `universal_night_shift_operator/SKILL.md` — the overnight execution coordinator
- `NIGHT_SHIFT.md` — the five-phase workflow (classify → split → route → execute → morning brief)
- `MORNING_BRIEF.md` — the exact output contract for the next-morning deliverable
- `SAFETY_RULES.md` — full allow/deny rules for what the night shift may and may not do
- `night_shift_manifest.json` — machine-readable registration of the night shift operator and its commands

Night Shift Mode is triggered by any of these commands:

```text
/run nightshift [objective]
/run overnight [objective]
/run morning-brief [objective]
/run founder-brief [objective]
```

The night shift operator may research, plan, draft, analyze, summarize, create specs, create tasks, and prepare recommendations. It will not deploy, spend money, publish content, send messages, sign contracts, delete data, expose secrets, or make irreversible decisions. Anything that requires those actions is presented in the Morning Brief under **Decisions Needed** for explicit human approval.
