# Grader Patterns

Use this reference when implementing graders for skill evaluation.

## Grader Types

### Deterministic Graders

Run a command and check the result. Fast, explainable, debuggable.

Output format (JSON to stdout):
```json
{
  "score": 0.67,
  "details": "2/3 checks passed",
  "checks": [
    { "name": "file-created", "passed": true, "message": "package.json exists" },
    { "name": "structure-correct", "passed": true, "message": "src/components/ present" },
    { "name": "build-passes", "passed": false, "message": "npm run build exited with code 1" }
  ]
}
```

`score` (0.0–1.0) and `details` are required. `checks` is optional but strongly recommended.

Common patterns:
- File existence: `test -f <path>`
- File content match: `grep -q "expected" <path>`
- Command in trace: parse JSONL trace for `command_execution` events
- Build success: run build command and check exit code
- Runtime probe: start server, `curl` the health endpoint, stop server

### LLM Rubric Graders

Evaluate qualitative aspects using a structured rubric. The LLM grades the skill's output against criteria you define.

Rubric structure:
```
Criterion Name (score range):
- What passes
- What fails
- Edge cases to consider
```

Example:
```
Workflow Compliance (0-0.5):
- Full marks: all 3 documented steps executed in order
- Partial: steps present but out of order
- Zero: mandatory steps skipped

Style Consistency (0-0.5):
- Full marks: all components follow declared conventions
- Partial: minor deviations in naming or formatting
- Zero: wrong technology stack or architecture pattern
```

Use structured output schemas to get stable, parseable results:
```json
{
  "type": "object",
  "properties": {
    "overall_pass": { "type": "boolean" },
    "score": { "type": "number", "minimum": 0, "maximum": 1 },
    "checks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "score": { "type": "number" },
          "pass": { "type": "boolean" },
          "notes": { "type": "string" }
        },
        "required": ["id", "score", "pass", "notes"]
      }
    }
  },
  "required": ["overall_pass", "score", "checks"]
}
```

### Combining Graders

Weight deterministic graders higher for objective checks, LLM graders for subjective checks.

Recommended split:
- 60-70% deterministic (did it work?)
- 30-40% LLM rubric (was the approach good?)

Final score: `Σ (grader_score × weight) / Σ weight`

## Trigger Test Patterns

### Positive Triggers

Test prompts that SHOULD activate the skill.

Categories:
1. Direct reference: `Use the $skill-name to do X`
2. Task description: `Set up X with Y for Z`
3. Noisy context: `I'm building a demo for the conference, can you scaffold X with Y`

### Negative Triggers

Test prompts that SHOULD NOT activate the skill.

Categories:
1. Adjacent task: similar domain but different action
2. Partial overlap: mentions the same tools but for a different purpose
3. Ambiguous: could go either way — document the expected behavior

## Static Analysis Checks

These run without executing the skill and catch structural issues early.

### Frontmatter Checks

| Check | Rule |
|-------|------|
| `name` present | Required by all platforms |
| `name` matches directory | Mandatory for OpenClaw, good practice everywhere |
| `description` present | Required by all platforms |
| `description` includes trigger phrasing | "Use when..." pattern |
| `description` length | 110-420 characters for optimal recall and scanning |
| `metadata` well-formed | Valid JSON if present |

### Structural Checks

| Check | Rule |
|-------|------|
| Referenced files exist | Every path in SKILL.md resolves to a real file |
| Commands use `{baseDir}` | Portable path references, not hardcoded |
| No dead internal links | `[text](path)` links point to existing files |
| Scripts are executable | Files in `bin/` and `scripts/` have proper shebangs |

### Content Quality Checks

| Check | Rule |
|-------|------|
| Example prompts present | At least 3 realistic user-style examples |
| Definition of done exists | Measurable completion criteria stated |
| Boundary clarity | Skill states what it does NOT do, or scope is unambiguous |
| Prerequisites listed | Environment variables, tools, and dependencies documented |
| Workflow documented | Step-by-step process described |

### Cross-Platform Readiness

| Check | Platform | What to verify |
|-------|----------|---------------|
| SKILL.md exists | OpenClaw, Claude Code, Codex | Core requirement |
| `name` is lowercase-hyphenated | OpenClaw | Naming constraint |
| `metadata.openclaw` valid | OpenClaw | JSON on single line |
| `agents/openai.yaml` exists | OpenAI Codex | UI metadata |
| `.cursor/rules/` or AGENTS.md | Cursor | Adapter files |
| SKILL.md or `.claude/` | Claude Code | Recognized paths |

## Eval Suite Design

Start with 10-20 prompts and grow from real failures.

Minimum coverage:
- 2-3 explicit trigger tests (should fire)
- 2-3 implicit trigger tests (should fire from task description)
- 1-2 negative trigger tests (should NOT fire)
- 2-3 outcome correctness tests
- 1-2 style compliance tests

Each test case should have:
- Unique ID
- Clear expected behavior
- Deterministic success criteria where possible
- LLM rubric for qualitative aspects

## CI Integration

Run evals on every skill change. Use `--ci` mode with a threshold.

Recommended workflow:
1. Push skill change
2. CI runs `eval_skill.py --json` for static analysis
3. CI runs eval suite with `--smoke` for quick validation
4. Nightly CI runs `--regression` for comprehensive testing
5. Block merge if any `critical` finding or if score drops below threshold
