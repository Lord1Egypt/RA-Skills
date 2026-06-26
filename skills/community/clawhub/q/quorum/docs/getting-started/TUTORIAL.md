# Tutorial: Your First Validation Run

This tutorial walks through validating a simple agent configuration using Quorum. It uses a deliberately flawed example so you can see what the critics catch.

---

## Setup

Clone the repo and navigate to the examples directory:

```bash
git clone https://github.com/SharedIntellect/quorum.git
cd quorum/examples/tutorial
```

---

## Step 1: The Artifact

We'll validate this agent configuration file (`bad-config.yaml`). It has several intentional issues.

> **Note:** Model names in these examples use Anthropic's Claude (e.g., `anthropic/claude-sonnet-4-6`). Substitute your preferred provider and model — Quorum is model-agnostic.

```yaml
# bad-config.yaml
swarm: research-swarm
version: 1.0

agents:
  - name: researcher
    role: researcher
    # Missing: model
    tools: [web_search, web_fetch, exec, file_read, file_write, agent_spawn]
    spawn_pattern: "run.sh $USER_QUERY"  # shell injection!

  - name: synthesizer
    model: anthropic/claude-sonnet-4-6
    role: synthesizer
    tools: [web_search, web_fetch, exec, file_read, file_write, message_send]
    # No output_contract

  - name: validator
    model: anthropic/claude-sonnet-4-6
    role: validator
    input: "{{ synthesizer_output }}"  # in-memory passing
```

Issues we planted:
1. `researcher` has no `model` assignment
2. `spawn_pattern` uses `$USER_QUERY` — shell injection vector
3. `researcher` has far too many tools (including `agent_spawn`)
4. `synthesizer` has no `output_contract`
5. `validator` receives input in-memory via template variable

---

## Step 2: Choose Rubric and Depth

We'll use the swarm config rubric at standard depth:

```bash
quorum run \
  --target bad-config.yaml \
  --rubric swarm-config \
  --depth standard
```

---

## Step 3: What Happens

1. **Supervisor** reads `bad-config.yaml`, loads `swarm-config-rubric.json`, writes `run-manifest.json`

2. **Three critics + Tester** run at standard depth:
   - **Correctness Critic:** No factual errors, but notes the version is 1.0 with no changelog
   - **Security Critic:** Finds `$USER_QUERY` in spawn pattern — CRITICAL injection vector
   - **Completeness Critic:** Finds missing `model` on researcher — CRITICAL gap
   - **Architecture Critic:** 🔜 *(Planned)* Would flag researcher having 6 tools (exec + agent_spawn are high-risk for a read-only role)
   - **Delegation Critic:** 🔜 *(Planned)* Would flag missing `output_contract` on synthesizer; in-memory template passing on validator

3. **Tester** ✅ verifies:
   - `grep -n '\$[A-Z]' bad-config.yaml` → confirms line 8 injection
   - Schema parse confirms missing `model` on researcher
   - Schema parse confirms `synthesizer` has no `output_contract`

4. **Fixer** generates fixes for the 2 CRITICAL issues

5. **Aggregator** merges and deduplicates findings

6. **Supervisor** writes verdict: **REVISE**

---

## Step 4: The Output

`verdict.json`:
```json
{
  "verdict": "REVISE",
  "coverage": "12/14 criteria evaluated",
  "summary": "2 CRITICAL, 3 HIGH, 1 MEDIUM findings. Shell injection and missing model assignment must be resolved before production use.",
  "issues": [
    {
      "id": "SEC-001",
      "severity": "CRITICAL",
      "location": "agents[0].spawn_pattern",
      "description": "Shell variable interpolation creates injection vector",
      "evidence": { "tool": "grep", "output": "run.sh $USER_QUERY (line 8)" },
      "fix": "Replace with file-based input: 'run.sh --input /tmp/query.json'"
    },
    {
      "id": "COMP-001",
      "severity": "CRITICAL",
      "location": "agents[0]",
      "description": "researcher agent has no model assignment",
      "evidence": { "tool": "grep", "output": "No 'model:' found in researcher block" },
      "fix": "Add 'model: anthropic/claude-sonnet-4-6' to researcher agent"
    },
    {
      "id": "ARCH-001",
      "severity": "HIGH",
      "location": "agents[0].tools",
      "description": "researcher has 6 tools including exec and agent_spawn — violates least-privilege",
      "evidence": { "tool": "schema_parse", "output": "tools: [web_search, web_fetch, exec, file_read, file_write, agent_spawn]" },
      "fix": "Reduce to: [web_search, web_fetch, file_write] — researcher only needs to search and write findings"
    }
    // ... more issues
  ]
}
```

---

## Step 5: The Fixed Config

After applying the Fixer's suggestions:

```yaml
# fixed-config.yaml
swarm: research-swarm
version: 1.1
changelog:
  - v1.1: Fixed shell injection, added model assignments, scoped tool permissions

agents:
  - name: researcher
    model: anthropic/claude-sonnet-4-6  # Added
    role: researcher
    tools: [web_search, web_fetch, file_write]  # Scoped down
    spawn_pattern: "run.sh --input /tmp/query.json"  # No interpolation
    output_contract:
      format: json
      schema: findings-schema.json
      path: runs/{run-id}/researcher-output.json

  - name: synthesizer
    model: anthropic/claude-sonnet-4-6
    role: synthesizer
    tools: [file_read, file_write]
    input_contract:
      source: runs/{run-id}/researcher-output.json  # File-based
    output_contract:
      format: markdown
      path: runs/{run-id}/synthesis.md

  - name: validator
    model: anthropic/claude-sonnet-4-6
    role: validator
    tools: [file_read]
    input_contract:
      source: runs/{run-id}/synthesis.md  # File-based, no template
```

Run validation again with the fixed config:

```bash
quorum run \
  --target fixed-config.yaml \
  --rubric swarm-config \
  --depth standard
```

Expected result: **PASS** (or PASS_WITH_NOTES on the remaining LOW issues)

---

## What You Just Saw

1. The **Security Critic** caught a shell injection that would have allowed user input to execute arbitrary commands
2. The **Completeness Critic** caught a missing model assignment that would have caused non-deterministic behavior
3. The **Architecture Critic** 🔜 would catch excessive tool permissions that violated least-privilege
4. The **Delegation Critic** 🔜 would catch in-memory passing that breaks parallelism and determinism
5. The **Tester** ✅ verifies every finding with actual tool output — no hand-waving
6. The **Fixer** gave you concrete, applicable changes

That's Quorum working as designed.

---

## Next Steps

- Try the research synthesis rubric on a LLM-generated report
- Write a custom rubric for your domain
- Run at `--depth thorough` for your next production deployment
- Check `known_issues.json` after a few runs — learning memory tracks recurring patterns across runs (shipped v0.5.3)

---

*Questions? [GitHub Discussions](https://github.com/SharedIntellect/quorum/discussions)*


---

> ⚖️ **LICENSE** — Not part of the operational specification above.
> This file is part of [Quorum](https://github.com/SharedIntellect/quorum).
> Copyright 2026 SharedIntellect. MIT License.
> See [LICENSE](https://github.com/SharedIntellect/quorum/blob/main/LICENSE) for full terms.
