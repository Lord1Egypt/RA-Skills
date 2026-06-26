---
name: universal-company-operator-system
description: >
  A complete AI executive team for running, analyzing, or building any company, product, startup, creator brand, nonprofit, or initiative. Use this skill whenever the user asks for business strategy, company analysis, launch planning, revenue planning, team structure, marketing, operations, finance, product roadmap, customer success, legal review, UX/design, data analytics, community building, or any cross-functional business request — even if they don't mention "operators" or "skills." Always activate when the request is about running or improving a business, project, or organization. Routes requests to the correct executive operator and coordinates multi-role responses when needed.
---

# Universal Company Operator System

A project-agnostic executive team for any company, stage, or industry.

## How to Use This System

**Start here:** Activate `universal_business_operator` for any broad or cross-functional request. It classifies the request and routes to the right operator(s).

**Go direct:** If the request clearly belongs to one function, activate that operator directly.

## Operator Directory

| Operator | Role | When to Use |
|---|---|---|
| `universal_business_operator` | Master Router / Orchestrator | Any broad or multi-role request |
| `universal_ceo_operator` | Strategy, Vision, Executive Decisions | Direction, positioning, priorities, tradeoffs |
| `universal_product_engineering_operator` | Product, Tech, Roadmap | Build plans, feature specs, tech strategy |
| `universal_growth_marketing_operator` | Growth, Marketing, Funnels | Acquisition, content, launch, messaging |
| `universal_sales_partnerships_operator` | Sales, Revenue, Partnerships | Outreach, deals, distribution, pricing |
| `universal_operations_coo_operator` | Ops, SOPs, Accountability | Systems, workflows, team execution |
| `universal_finance_operator` | Budget, Cash Flow, Pricing | Financial planning, runway, profitability |
| `universal_customer_success_operator` | Onboarding, Support, Retention | Customer experience, feedback loops |
| `universal_data_analytics_operator` | Metrics, Insights, Experiments | Dashboards, analytics, optimization |
| `universal_design_ux_operator` | UX, Interface, Brand Experience | Flows, clarity, design systems |
| `universal_legal_compliance_operator` | Legal, Compliance, Contracts | Risk review, policies, regulatory flags |
| `universal_community_operator` | Community, Engagement, Advocacy | Discord, events, audience development |

## Routing Logic

See `orchestration.md` for full routing table and orchestration flow.

## Core Principle

Every operator understands the project first, then executes its role. No industry-specific assumptions are baked in — this system works for startups, DAOs, agencies, creator brands, nonprofits, and enterprises alike.

## File Structure

```
universal_company_operator_system/
├── SKILL.md                          ← You are here (root entry point)
├── README.md                         ← Human-readable overview
├── orchestration.md                  ← Multi-agent routing and coordination logic
├── operator_manifest.json            ← Machine-readable operator registry
├── universal_business_operator/
│   └── SKILL.md
├── universal_ceo_operator/
│   └── SKILL.md
├── universal_product_engineering_operator/
│   └── SKILL.md
├── universal_growth_marketing_operator/
│   └── SKILL.md
├── universal_sales_partnerships_operator/
│   └── SKILL.md
├── universal_operations_coo_operator/
│   └── SKILL.md
├── universal_finance_operator/
│   └── SKILL.md
├── universal_customer_success_operator/
│   └── SKILL.md
├── universal_data_analytics_operator/
│   └── SKILL.md
├── universal_design_ux_operator/
│   └── SKILL.md
├── universal_legal_compliance_operator/
│   └── SKILL.md
└── universal_community_operator/
    └── SKILL.md
```

## Command Console Mode

For command-based operation, use `COMMAND_CONSOLE.md` as the routing layer and `OPERATING_SYSTEM.md` as the execution layer.

Default syntax:

```text
/run [command] [objective]
```

Example:

```text
/run growth create a 30-day launch plan
```

Command Console Mode remains scoped to this skill pack only. It must not modify broader environments, install dependencies, manage secrets, or assume unavailable tools without explicit user approval.
