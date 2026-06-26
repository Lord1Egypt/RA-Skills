# Copilot CLI Port — Architecture Mapping

How Quorum's reference implementation components map to Copilot CLI primitives.

---

## Component-Level Mapping

### Supervisor → SKILL.md Orchestration

The reference implementation's `supervisor.py` selects critics based on depth profile and artifact type. In the Copilot port, this logic moves into SKILL.md as natural language instructions that Copilot follows to orchestrate the validation flow.

```
Reference:  supervisor.py → selects critics → ThreadPoolExecutor → collects results
Copilot:    SKILL.md instructions → spawns task agents → collects responses
```

### Critics → Task Agents

Each critic's system prompt + rubric injection becomes a `task` agent call:

```python
# Reference implementation (simplified)
critic_result = litellm.completion(
    model=config.tier2_model,
    messages=[system_prompt + rubric + artifact]
)

# Copilot CLI equivalent (conceptual)
critic_result = task(
    agent_type="explore",  # or "general-purpose" for security
    model="sonnet",
    prompt=system_prompt + rubric + artifact
)
```

### Pre-Screen → Script Execution

The pre-screen layer runs identically — it's already a Python script that shells out to external tools:

```
Reference:  quorum run → pre_screen.py → [DevSkim, Ruff, Bandit, PSSA]
Copilot:    SKILL.md → python quorum-prescreen.py → [DevSkim, Ruff, Bandit, PSSA]
```

**Key difference:** Pre-screen must be stdlib-only for the port. The reference implementation uses pyyaml for config parsing — make it optional with JSON fallback.

### Aggregator → SKILL.md Logic or Dedicated Agent

The aggregator merges findings, resolves conflicts, and assigns verdicts. Two options:

1. **Inline in SKILL.md** — aggregation logic as natural language instructions. Simpler, fewer premium requests.
2. **Dedicated agent** — `general-purpose` agent with aggregator prompt. More robust for complex conflict resolution.

Recommendation: Start with option 1, move to option 2 if quality suffers.

### Fixer → General-Purpose Agent

The fixer needs write access to propose changes:

```
Reference:  fixer.py → reads findings + artifact → proposes text replacements → writes fix-proposals.json
Copilot:    general-purpose task agent → reads findings + artifact → proposes changes → writes to disk
```

### Learning Memory → File Persistence

`known_issues.json` is read at session start and written after verdict. Files persist across Copilot sessions — no changes needed to the data format.

### Cost Tracking → Not Applicable

LiteLLM cost tracking doesn't apply. Copilot uses premium requests, not per-token billing. The port should track premium request count instead.

### Batch Validation → Sequential Task Dispatch

The reference implementation's batch mode processes multiple files with crash-resilient progressive saves. In Copilot:

```
Reference:  BatchVerdict → ThreadPoolExecutor(max_workers=3) → progressive manifest
Copilot:    SKILL.md loops over files → sequential or parallel task dispatch → progressive file writes
```

---

## Prompt Extraction Guide

When extracting critic prompts from Python classes, preserve:

1. **System prompt** — the critic's identity, evaluation criteria, and output format requirements
2. **Rubric injection** — how rubric criteria are formatted and injected into the prompt
3. **Evidence grounding instruction** — the requirement to cite specific locus (file, line, excerpt) for every finding
4. **Output schema** — the JSON structure critics must return (findings array with severity, location, criterion, evidence)

Do NOT extract:
- LiteLLM-specific code (model routing, retry logic, cost tracking)
- ThreadPoolExecutor orchestration (replaced by `task` agents)
- File I/O wrappers (Copilot agents handle file operations natively)

---

## Testing Strategy

### Equivalence Testing

For each critic, run the same artifact through both:
1. Reference implementation (`quorum run --target <file> --depth standard`)
2. Copilot CLI port (natural language invocation)

Compare: finding count, severity distribution, evidence quality, verdict. They should converge but won't be identical (different model access patterns, prompt formatting).

### Regression Artifacts

Use the reference implementation's existing test artifacts:
- `examples/sample-research.md` — planted flaws for research validation
- `examples/bad-config.yaml` — planted security + completeness issues
- Golden set artifacts (if graduated to public)

### Platform-Specific Testing

- Windows native PowerShell (primary)
- WSL (secondary)
- macOS Terminal (tertiary)
- Linux (tertiary)
