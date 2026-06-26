# supplier-risk-scorecard

Assess a supplier's risk profile across five standardized dimensions and produce a scored risk scorecard with a risk-tier rating and a prioritized mitigation action plan.

## When to use

Use this skill when:
- Onboarding a new supplier and need a structured risk baseline
- Conducting an annual or triggered supplier review
- A disruption signal (news, audit finding, geopolitical event) warrants a rapid re-assessment
- Procurement or sourcing leadership needs a risk-tiered supplier ranking

## What it delivers

- A completed risk scorecard table (five dimensions, each scored 1–5)
- An overall risk tier: Low / Medium / High / Critical
- The top three risk flags with supporting evidence
- A prioritized mitigation action plan (owner, action, timeline)
- An evidence-gap log noting which scores rely on assumptions

## Inputs expected

| Input | Required? |
|---|---|
| Supplier name and legal entity | Yes |
| Country of incorporation / primary operations | Yes |
| Category or commodity supplied | Recommended |
| Tier level (Tier 1 / Tier 2) | Recommended |
| Estimated annual spend | Optional |
| Supporting documents (financials, audit reports, certifications, delivery data) | Optional — skill works without them |

## Safety notes

- Never fabricates financial data, audit results, or country risk scores.
- Scores missing dimensions conservatively and flags every assumption explicitly.
- Does not request system credentials, login access, or internal database exports.
- Personal employee data in shared documents is not quoted or retained in output.
- Sanctioned entities or confirmed regulatory violations are always escalated to Critical tier.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.