---
name: strategic-mentality
description: Apply battle-tested business mentality frameworks from Sun Tzu (Art of War), Alex Hormozi ($100M Leads), The 12 Week Year, and Dan Kennedy (No BS Direct Response) to real business decisions. Includes automated weekly accountability scorecards, mentality-weighted lead scoring, sales call objection handling, and optional business context overlays. Use this skill when the user needs strategic advice, wants to evaluate a business opportunity, plan a sprint, design offers or lead generation, assess competition, structure outreach, make pricing decisions, score a lead, handle sales objections, or think through any business problem using proven frameworks. Triggers on phrases like "analyze this strategically", "what would Hormozi do", "help me plan my 12 weeks", "evaluate this opportunity", "score this lead", "how do I handle this objection", "apply a framework", "weekly scorecard", or any request that benefits from structured strategic thinking instead of generic advice.
version: 1.1.0
---

# Strategic Mentality System

Apply decision frameworks from four master sources to real business problems. No philosophy quotes, no motivational fluff. Actionable heuristics, concrete next actions, structured output.

## Available Mentalities

Read the relevant reference file in `references/` before applying any framework.

| Mentality | File | Use When | Core Question |
|---|---|---|---|
| **SUN_TZU** | `references/sun-tzu.md` | Competition, positioning, market entry, timing, resource allocation | "How do I win without wasting resources?" |
| **HORMOZI** | `references/hormozi.md` | Lead generation, offers, pricing, advertising, scaling, outreach | "How do I get more strangers to want to buy my stuff?" |
| **TWELVE_WEEK** | `references/twelve-week.md` | Sprint planning, accountability, execution scoring, time blocking | "Am I executing on what matters this week?" |
| **DAN_KENNEDY** | `references/dan-kennedy.md` | Sales psychology, urgency, direct response, closing reluctant buyers | "How do I get them off the fence right now?" |

## Specialized Modules

| Module | File | Use When |
|---|---|---|
| **Lead Scoring** | `references/lead-scoring.md` | Evaluate any lead with a 0-100 mentality-weighted score |
| **Sales Call** | `references/sales-call.md` | Handle objections during sales calls, especially with SME owners |
| **Nex AI Context** | `references/nex-ai-context.md` | Auto-load when running in Nex AI's OpenClaw instance for calibrated recommendations |

## Weekly Accountability

The `HEARTBEAT.md` file configures a scheduled Sunday evening ping via Telegram with a 12 Week Year scorecard prompt. The agent asks the user to fill in their weekly score, reviews the trend, and flags if execution is slipping below 65%.

## How to Apply

### Step 1: Map the Problem

| Problem Type | Primary | Support |
|---|---|---|
| Should I pursue this lead/client? | HORMOZI | SUN_TZU |
| How do I beat competitor X? | SUN_TZU | HORMOZI |
| I'm not making progress | TWELVE_WEEK | SUN_TZU |
| What should I build/sell next? | HORMOZI | TWELVE_WEEK |
| How do I plan my next quarter? | TWELVE_WEEK | HORMOZI |
| Should I pivot or stay the course? | SUN_TZU | TWELVE_WEEK |
| How do I price this? | HORMOZI | SUN_TZU |
| I'm spread too thin | TWELVE_WEEK | SUN_TZU |
| How do I outreach effectively? | HORMOZI | DAN_KENNEDY |
| Score this lead | Lead Scoring module | All mentalities |
| Handle sales objection | Sales Call module | DAN_KENNEDY |
| Close this deal | DAN_KENNEDY | HORMOZI |
| Follow up strategy | DAN_KENNEDY | TWELVE_WEEK |

### Step 2: Load the Reference File

Read the matching `references/*.md` file. Each contains core principles, if-then heuristics, diagnostic questions, and an output template.

### Step 3: Run Diagnostics

Ask the diagnostic questions from the loaded mentality to map the user's specific situation.

### Step 4: Apply Heuristics and Output

Run the situation through the if-then heuristics. Output:

1. **Situation Assessment** - 2-3 sentences mapping problem to framework
2. **Framework Verdict** - what the mentality says to do
3. **Concrete Actions** - specific next steps with measurable targets
4. **Risk** - what could go wrong

### Step 5: Combine When Needed

For complex decisions, apply the PRIMARY mentality first, then layer the SUPPORT mentality as a constraint or amplifier. Flag any contradictions explicitly.
