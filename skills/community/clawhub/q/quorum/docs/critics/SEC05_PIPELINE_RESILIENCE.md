# SEC-05: Pipeline Resilience and Adversarial Inputs

**Status:** Stub
**Author:** Akkari (with Daniel Cervera)
**Date:** 2026-03-09
**Scope:** Threat model for attacks targeting the validation pipeline's operational integrity — distinct from evidence fabrication (SEC-03)

**Origin:** Identified during SEC-03 review. The question "has there ever been a buffer overflow attack via feeding an AI model?" surfaced a class of threats where the goal isn't to pass validation but to *break or degrade* it.

---

## Distinction from SEC-03

**SEC-03** asks: *Is the evidence real, adequate, and authoritative?*
**SEC-05** asks: *Can the pipeline itself be subverted, exhausted, or degraded?*

SEC-03 threats want a PASS. SEC-05 threats may want a failure — denial of validation is itself a win if it blocks or delays an assessment.

---

## Attack Vectors (to develop)

### Context Window Exhaustion
Artifact so large it fills the critic's context window, pushing rubric criteria and system prompt out of effective attention. Analogous to buffer overflow in spirit — overwhelm a fixed-capacity resource to bypass controls.

### Parser Exploitation
Deeply nested or malformed YAML/JSON/structured data designed to crash or hang the pre-screen layer before critics are ever invoked.

### Output Corruption
Artifact content designed to make critics produce malformed output that the aggregator can't parse — causing crashes, timeouts, or silent null verdicts propagating downstream.

### Cost/Budget Exhaustion
Repeated or oversized submissions designed to burn through `--max-cost` budget on garbage artifacts, leaving no budget for real validation. A resource exhaustion attack on the economic layer.

### Denial of Validation
Any combination of the above used not to pass, but to prevent or delay a legitimate assessment from completing.

---

## Existing Defenses (audit needed)

- `--max-cost` cap (limits economic exposure)
- Crash-resilient batch with `--resume` and SIGTERM handler (limits blast radius)
- Pre-screen runs before LLM critics (deterministic gate)
- Timeout on individual critic runs

## Open Questions

- What are the actual context window limits per model, and does the pipeline enforce artifact size limits before sending to critics?
- Can a malformed artifact cause the aggregator to produce a verdict of None? (Possible connection to the verdict.json None bug)
- Should the pre-screen include an artifact size/complexity gate?
- How does `--max-cost` interact with adversarial inputs that are cheap to submit but expensive to evaluate?

---

## References

- SEC-03 — Evidence Integrity and Anti-Gaming (companion threat model)
- SEC-04 — Threat context relationships
- Anthropic, "Many-shot Jailbreaking" (2024) — context window manipulation research
- OWASP LLM Top 10 — LLM01 (Prompt Injection), LLM04 (Denial of Service)
