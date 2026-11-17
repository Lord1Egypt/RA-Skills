# results-claim-hedging-checker

A WorkBuddy / CodeBuddy skill that audits the **Results section** of psychology and STEMM research papers for five recurring problem types:

| Dimension | What it checks |
|---|---|
| D1 — Hedging | Missing or excessive hedging around indirect evidence |
| D2 — Claim Strength vs. Evidence | Overclaims beyond statistical support; causal leaps from correlational data |
| D3 — Causal Language | Causal verbs mismatched to the research design |
| D4 — Interpretation in Results | Theoretical explanation, hypothesis restatement, or conclusions leaking into Results |
| D5 — Subjective Language | Evaluative adjectives, subjective lead-ins, absolute expressions |

**Scoring**: 1–5 per dimension (5 = no issues, 1 = severe problems). Cross-dimension composite takes the lowest score.

The diagnosis is grounded in **18 curated examples (F-01 ~ F-18) from 8 classic psychology papers** (Milgram 1963; Festinger & Carlsmith 1959; Loftus & Palmer 1974; Elkin et al. 1989; Costa & McCrae 1988; Cohen et al. 1983; Asch 1956; Ainsworth & Bell 1970).

## Repository structure

```
├── SKILL.md                       # Main skill definition (workflow, rubric, output format)
├── references/
│   ├── rubric.md                  # 1–5 scoring criteria per dimension
│   ├── checklist.md               # 6-stage diagnostic checklist
│   └── examples/
│       └── examples_memberF.md    # 18 examples (F-01 ~ F-18)
├── test_input_01.md               # Test: structural priming Results (clean draft)
├── test_input_02.md               # Test: mindfulness intervention Results (problem draft)
├── test_output_01.md              # Audit report for test input 01
└── test_output_02.md              # Audit report for test input 02
```

## Output format

Every audit uses six standardized headings so it can be merged by an aggregator skill:

1. Dimension Score
2. Key Problems
3. Evidence from Draft
4. Example-based Comparison
5. Revision Suggestions
6. Priority Level

## Scope boundary

Statistical reporting format (effect sizes, confidence intervals, completeness of statistical notation) is **out of scope** and delegated to a companion skill, `results-statistics-convention-checker`.

Causal-language trigger words that describe participant behavior (e.g., "participants produced responses") rather than causal inference are exempted from D3 flags.
