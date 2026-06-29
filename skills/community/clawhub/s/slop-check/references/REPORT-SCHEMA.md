# REPORT-SCHEMA.md — the payload you write for the report

You never read or write HTML. Write this JSON to `<target-root>/.slop-check/report-data.json`,
then run `scripts/build-report.mjs`. It validates the payload and injects it into the template;
if it rejects the payload, fix what it names and rerun.

```jsonc
{
  "project": {
    "name": "repo-name",
    "root": "path or repo url",
    "date": "YYYY-MM-DD",
    "filesAnalyzed": 239,          // from metrics.json totals.codeFiles
    "codeLines": 39512,            // from metrics.json totals.codeLines
    "languages": [{ "name": "TypeScript", "pct": 99.7 }, { "name": "JavaScript", "pct": 0.3 }]
    // Copy this verbatim from metrics.json `totals.languagePercents` — already named,
    // sorted, and rounded to one decimal place. Decimals are intentional: a repo that's
    // 99.7% TS / 0.3% JS should show both, not round the minor language away.
  },
  "slopPercent": 16,               // integer 0-100, computed per SCORING.md
  "tier": {
    "name": "Mid-Level Engineer",  // exact tier name from SCORING.md bands
    "blurb": "Genuinely fine. Also, slightly mid.",   // exact blurb from SCORING.md
    "easterEgg": false             // true ONLY when slopPercent <= 3
  },
  "verdict": "One paragraph. Deadpan, specific, quotable. Must contain the single most damning or most impressive concrete fact found.",
  "fastestClimb": "One sentence naming the single most valuable thing to do — the fix with the biggest quality payoff, in plain terms. Lead with the action and describe the payoff qualitatively. Do NOT put percentages or point numbers in this text (no '44% -> 38%', no '~5 pts'). Shown under the 'Where to Start' heading.",
  "categories": [                  // all 7, weights must sum to 100
    {
      "name": "Architecture & Modularity",
      "weight": 25,
      "score": 22,                 // 0-100 slop for this category
      "source": "judgment",        // "judgment" or "script"
      "note": "One line explaining the score."
    }
  ],
  "findings": [                    // every deduction, worst first; 6-20 typical
    {
      "category": "Duplication",
      "severity": "major",         // "minor" | "moderate" | "major"
      "points": 10,
      "file": "src/foo.ts",        // repo-relative path
      "line": 142,                 // null if file-level
      "description": "One line. Specific. Cites what is actually there."
    }
  ],
  "fixItPrompts": [                // 3-6, ordered by impact; the genuinely-useful payoff
    {
      "title": "Merge the copy-pasted extractors",
      "pointsWorth": 2,            // value magnitude, used to ORDER prompts and pick a ★ badge — never shown as a raw number. List prompts high-to-low.
      "prompt": "Three parts, per SKILL.md step 5: (1) the task — files, problem, desired end state, verification; (2) a 'Context from the slop-check map:' block embedding the target's importedBy/imports lists from slop-map.json plus relevant reviewer observations and related findings, so the fixing agent starts warm; (3) the closing pointer to .slop-check/slop-map.json for the full import map."
    }
  ],
  "stats": {                       // straight from metrics.json
    "cycles": 1, "godFiles": 9, "orphans": 4, "dupPercent": 5.9, "aiTells": 0
  }
}
```
