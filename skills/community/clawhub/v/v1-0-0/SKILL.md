---
name: deeptechnic-dd
description: >
  Deep-tech due diligence framework. Guides investment DD agents through independent
  technical validation, team assessment, supply chain audit, and competitor discovery.
  Use when evaluating hard-tech startup projects, reviewing BP technical claims, or
  conducting pre-investment technology risk assessment.
---

# Deeptechnic — Technical Due Diligence Framework

A structured system for conducting independent technology due diligence on hard-tech startup investments. The system follows a four-round iterative workflow and evaluates projects across 10 quality dimensions.

> **This is a meta-skill.** It bundles sub-skills as references. Load the relevant reference for your current phase.

## When to Use

- Evaluating a hard-tech startup's BP/technical claims
- Conducting a first-pass technical assessment before expert interviews
- Reviewing team capability gaps and supply chain risks
- Generating structured due diligence reports

**Not for:** Financial due diligence, legal due diligence, or final investment decisions.

## Quick Start

```
1. Load references/skills-index.md to see available sub-skills
2. For current phase, load the corresponding reference skill(s):
   - 1st round:   load references/skills/deep-tech-dd-analysis + references/skills/anti-rationalization
   - 2nd round:   load references/skills/team-assessment + references/skills/supply-chain-audit
   - 3rd round:   load references/agents/tech-reviewer + agents/competition-analyst
   - Before output: load references/skills/quality-gate
   - After delivery: load references/skills/feedback-collection
3. Follow the Process steps in each loaded skill
4. Run quality gate before final output
```

## The 10 Quality Dimensions

Every assessment is scored against these dimensions (0.0-1.0):

| # | Dimension | Weight | Description |
|---|-----------|--------|-------------|
| 1 | claim_validation | 0.20 | Independent physics-based validation of tech claims |
| 2 | engineering_migration_gap | 0.15 | Analysis of lab-to-product engineering gaps |
| 3 | per_person_assessment | 0.15 | Per-member team capability matching |
| 4 | independent_competitor | 0.10 | BP-independent competitor discovery |
| 5 | supplier_level_analysis | 0.10 | Supplier-level supply chain audit |
| 6 | independent_analysis | 0.10 | Independent vs BP-derived analysis |
| 7 | team_gap_precision | 0.05 | Precision of structural gap identification |
| 8 | quantitative_score | 0.05 | Decimal-precision scoring (3.5/5 vs 4/5) |
| 9 | priority_levels | 0.05 | P0/P1/P2 question prioritization |
| 10 | overview_page | 0.05 | Executive summary on page one |

## Core Rules

1. Every tech claim must have independent physics-based verification (formula + calculation)
2. Team assessment must name each member individually with capability matching
3. Competitor analysis must independently verify BP's claims (never trust BP's competitor list)
4. Supply chain analysis must name specific suppliers, not generic "domestic alternatives"
5. All output must pass the 10-point quality gate before delivery
6. User feedback must be captured and structured as training data after each delivery

## Workflow

### Round 1 (First Pass)
- Collect public info (papers, patents, news)
- Validate core tech claims (formula + calculation)
- Assess first team capability
- Generate question list for team

### Round 2 (After Team Feedback)
- Refresh model with team's answers
- Generate expert interview outline + supply chain questions

### Round 3 (External Input)
- Cross-validate multiple sources
- Compile interview records

### Round 4 (Final)
- Synthesize all findings
- Generate comprehensive DD report

## Output Format

Reports follow this structure:
1. Overview page (mandatory): Claim judgment table + core rating
2. Technical analysis
3. Team assessment
4. Supply chain analysis
5. Competitive landscape
6. Comprehensive evaluation
7. Open questions (P0/P1/P2)
8. Next round recommendations

Report file naming: `Deeptechnic_<ProjectEngName>_<Phase>_<Date>.docx`

## Anti-Rationalization

Claims you may be tempted to make — and why they're wrong:

| "I don't need to verify every claim" | Missed physical impossibility → failed investment |
| "The BP's competitor list is enough" | BPs selectively omit domestic competitors |
| "Team bio looks good, skip verification" | Cannot verify without public sources |
| "This is just a quick pass" | First impressions lock in; do it right the first time |

## Red Flags

- All claim indicators are integers (no real test data)
- BP describes features without technical specifications
- Multiple extreme specs claimed simultaneously
- No third-party data anywhere in the BP
- BP competitor chart shows "all wins, no losses"
- "Confidential" used as reason to hide core data

## Verification

- [ ] All 6 core rules applied
- [ ] Quality gate passed before output
- [ ] Feedback recorded after delivery
- [ ] Training data appended to SkillOpt dataset
