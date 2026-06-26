# JSON Schemas

This document defines the JSON schemas used by skill-rules-designer evals.

---

## evals.json

Defines the eval test cases. Located at `evals/evals.json`.

```json
{
  "skill_name": "skill-rules-designer",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Human-readable description of success",
      "files": [],
      "expectations": [
        "The skill presents a plan before writing files",
        "At least one rules/*.md file is created"
      ]
    }
  ]
}
```

**Fields:**
- `skill_name`: Name matching the skill's frontmatter
- `evals[].id`: Unique integer identifier
- `evals[].prompt`: The task to execute
- `evals[].expected_output`: Human-readable description of success
- `evals[].files`: Optional list of input file paths
- `evals[].expectations`: List of verifiable assertions (pass/fail)

---

## grading.json

Output from the grader agent. Located at `<run-dir>/grading.json`.

```json
{
  "expectations": [
    {
      "text": "Presents a restructuring plan before writing any files",
      "passed": true,
      "evidence": "The transcript shows the plan was printed and user said 'go' before any Write tool calls."
    },
    {
      "text": "Creates at least one new rules/*.md file",
      "passed": false,
      "evidence": "No Write tool calls to rules/ directory found in transcript."
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 1,
    "total": 2,
    "pass_rate": 0.50
  },
  "execution_metrics": {
    "tool_calls": {
      "Read": 3,
      "Write": 1,
      "Edit": 0,
      "Bash": 0
    },
    "total_tool_calls": 4,
    "total_steps": 4,
    "errors_encountered": 0,
    "output_chars": 2800,
    "transcript_chars": 5200
  },
  "timing": {
    "executor_duration_seconds": 95.0,
    "grader_duration_seconds": 18.0,
    "total_duration_seconds": 113.0
  },
  "claims": [
    {
      "claim": "The restructuring is lossless",
      "type": "quality",
      "verified": true,
      "evidence": "All content removed from SKILL.md appears verbatim in the new rules file."
    }
  ],
  "user_notes_summary": {
    "uncertainties": [],
    "needs_review": [],
    "workarounds": []
  },
  "eval_feedback": {
    "suggestions": [],
    "overall": "No suggestions, evals look solid."
  }
}
```

**Fields:**
- `expectations[]`: Graded expectations with evidence
- `summary`: Aggregate pass/fail counts
- `execution_metrics`: Tool usage statistics
- `timing`: Wall clock timing (from timing.json)
- `claims`: Extracted and verified claims from the output
- `user_notes_summary`: Issues flagged by the executor
- `eval_feedback`: Optional improvement suggestions for the evals

---

## timing.json

Wall clock timing for a run. Located at `<run-dir>/timing.json`.

**How to capture:** When a subagent task completes, the task notification includes `total_tokens` and `duration_ms`. Save these immediately — they are not persisted elsewhere.

```json
{
  "total_tokens": 42500,
  "duration_ms": 95000,
  "total_duration_seconds": 95.0,
  "executor_start": "2026-03-10T10:30:00Z",
  "executor_end": "2026-03-10T10:31:35Z",
  "executor_duration_seconds": 95.0,
  "grader_start": "2026-03-10T10:31:36Z",
  "grader_end": "2026-03-10T10:31:54Z",
  "grader_duration_seconds": 18.0
}
```

---

## benchmark.json

Output from the AB comparison. Located at `<workspace>/benchmark.json`.

```json
{
  "metadata": {
    "skill_name": "skill-rules-designer",
    "skill_a_path": "/path/to/version-A",
    "skill_b_path": "/path/to/version-B",
    "timestamp": "2026-03-10T10:30:00Z",
    "evals_run": [1, 2, 3],
    "runs_per_configuration": 1
  },
  "runs": [
    {
      "eval_id": 1,
      "eval_name": "compress-and-encapsulate",
      "configuration": "version_a",
      "run_number": 1,
      "result": {
        "pass_rate": 0.86,
        "passed": 6,
        "failed": 1,
        "total": 7,
        "time_seconds": 95.0,
        "tokens": 42500,
        "tool_calls": 12,
        "errors": 0
      },
      "expectations": [
        {"text": "Presents a plan before writing files", "passed": true, "evidence": "..."}
      ],
      "notes": []
    }
  ],
  "run_summary": {
    "version_a": {
      "pass_rate": {"mean": 0.86, "stddev": 0.05, "min": 0.80, "max": 0.90},
      "time_seconds": {"mean": 95.0, "stddev": 8.0, "min": 85.0, "max": 105.0},
      "tokens": {"mean": 42500, "stddev": 3000, "min": 38000, "max": 46000}
    },
    "version_b": {
      "pass_rate": {"mean": 0.71, "stddev": 0.07, "min": 0.60, "max": 0.80},
      "time_seconds": {"mean": 78.0, "stddev": 6.0, "min": 70.0, "max": 86.0},
      "tokens": {"mean": 31000, "stddev": 2500, "min": 27000, "max": 35000}
    },
    "delta": {
      "pass_rate": "+0.15",
      "time_seconds": "+17.0",
      "tokens": "+11500"
    }
  },
  "notes": [
    "Version A scores higher on plan-before-write assertions across all 3 evals",
    "Version B is faster and uses fewer tokens but misses losslessness checks",
    "Eval 2 (harden) shows the largest quality gap: A=100%, B=57%"
  ]
}
```

**Important:** The viewer reads `configuration`, `result.pass_rate`, `result.time_seconds`, `result.tokens` with these exact field names. Use `version_a` / `version_b` as configuration identifiers for AB comparison (or `with_skill` / `without_skill` for baseline comparison).

---

## comparison.json

Output from the blind comparator agent. Located at `<grading-dir>/comparison-N.json`.

```json
{
  "winner": "A",
  "reasoning": "Output A follows the lossless restructuring principle — all moved content appears in the new rules file and SKILL.md references it. Output B drops the harden section without a destination file.",
  "rubric": {
    "A": {
      "content": {"correctness": 5, "completeness": 5, "accuracy": 4},
      "structure": {"organization": 4, "formatting": 5, "usability": 4},
      "content_score": 4.7,
      "structure_score": 4.3,
      "overall_score": 9.0
    },
    "B": {
      "content": {"correctness": 3, "completeness": 2, "accuracy": 3},
      "structure": {"organization": 3, "formatting": 3, "usability": 3},
      "content_score": 2.7,
      "structure_score": 3.0,
      "overall_score": 5.7
    }
  },
  "output_quality": {
    "A": {
      "score": 9,
      "strengths": ["Lossless restructuring maintained", "Clear references added to SKILL.md", "Token savings estimated"],
      "weaknesses": ["Minor: could have combined two small rules files"]
    },
    "B": {
      "score": 5,
      "strengths": ["Created a rules file", "Shortened SKILL.md"],
      "weaknesses": ["Dropped harden section without destination", "No reference added to SKILL.md", "No token savings estimate"]
    }
  }
}
```

---

## analysis.json

Output from the post-hoc analyzer. Located at `<grading-dir>/analysis.json`.

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/version-A",
    "loser_skill": "path/to/version-B",
    "comparator_reasoning": "Version A maintained losslessness; Version B dropped content without a destination"
  },
  "winner_strengths": [
    "Explicit losslessness check in plan step catches omissions before files are written",
    "Reference block in SKILL.md keeps context intact even after restructuring"
  ],
  "loser_weaknesses": [
    "No losslessness check meant content was dropped silently",
    "Vague 'move content as needed' instruction led to content loss"
  ],
  "instruction_following": {
    "winner": {"score": 9, "issues": ["Minor: skipped line count estimate in summary"]},
    "loser": {"score": 5, "issues": ["Did not add reference to SKILL.md after creating rules file", "Did not confirm with user before writing"]}
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "Add explicit losslessness check step: before removing from SKILL.md, verify the content exists verbatim in the destination file",
      "expected_impact": "Would prevent silent content loss"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "Read SKILL.md → Analyzed 4 dimensions → Presented plan → Waited for confirmation → Wrote rules file → Updated SKILL.md references → Printed summary",
    "loser_execution_pattern": "Read SKILL.md → Immediately started writing → Created rules file → Removed from SKILL.md but forgot to add reference"
  }
}
```
