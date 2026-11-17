# OWASP mapping

Sources: OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10, Dec 2025); OWASP *Agentic AI – Threats and Mitigations* v1.1 (threats T1–T17, Playbooks 1–6, Dec 2025); OWASP Top 10 for LLM Applications 2025 (LLM01–LLM10).

Use this file to label findings in the report and to sanity-check that no OWASP risk was skipped.

## Criteria → OWASP

| Criterion | ASI 2026 | Threats (T&M v1.1) | LLM 2025 | Playbook |
|---|---|---|---|---|
| C1 Identity & least privilege | ASI03 | T3, T9 | LLM06 | 4 |
| C2 Approval gates | ASI09, ASI02 | T10, T15, T7 | LLM06 | 5 |
| C3 Tool & action scoping | ASI02 | T2, T3 | LLM06 | 3 |
| C4 Code-execution isolation | ASI05 | T11 | LLM05 | 3 |
| C5 Untrusted input blast radius | ASI01, ASI09, ASI07 | T6, T12, T15, T7 | LLM01 | 1 |
| C6 Memory, context & config integrity | ASI06 | T1, T5 | LLM04, LLM08 | 2 |
| C7 Third-party extensions | ASI04 | T17 | LLM03 | 3 |
| C8 Secrets & sensitive data | ASI03 | T9 | LLM02, LLM07 | 4 |
| C9 Audit & traceability | ASI10 (detection) | T8 | — | 1 (step 3) |
| C10 Limits & kill switch | ASI08, ASI10 | T4, T13 | LLM10 | 3 |

## OWASP → criteria (coverage check)

| ASI 2026 | Primary | Also |
|---|---|---|
| ASI01 Agent Goal Hijack | C5 (worst case if hijacked) | C2 (gate catches hijacked actions), C6 (persistent hijack) |
| ASI02 Tool Misuse & Exploitation | C3 | C2, C4 |
| ASI03 Identity & Privilege Abuse | C1 | C8 |
| ASI04 Agentic Supply Chain | C7 (runtime-loaded extensions) | C6 (repo-controlled config adds tools); the project's own build dependencies are out of scope |
| ASI05 Unexpected Code Execution | C4 | C7 (code loaded as extensions) |
| ASI06 Memory & Context Poisoning | C6 | C5 |
| ASI07 Insecure Inter-Agent Communication | C5 (messages from other agents are untrusted input) | C1 (authority of whoever sends instructions) |
| ASI08 Cascading Failures | C10 (limits stop runaway chains) | C6 (cascading hallucination via memory) |
| ASI09 Human-Agent Trust Exploitation | C2 (what the approver sees) | C5 (rendered output as exfil/manipulation channel) |
| ASI10 Rogue Agents | C10 (kill switch) | C9 (detection), C1 (bounded privilege) |

| T&M threat | Criterion |
|---|---|
| T1 Memory Poisoning | C6 |
| T2 Tool Misuse | C3, C2 |
| T3 Privilege Compromise | C1 |
| T4 Resource Overload | C10 |
| T5 Cascading Hallucination | C6, C10 |
| T6 Intent Breaking & Goal Manipulation | C5 |
| T7 Misaligned & Deceptive Behaviors | C2, C9 (only deterministic controls are scorable statically) |
| T8 Repudiation & Untraceability | C9 |
| T9 Identity Spoofing / Agent Identity Compromise | C1, C8 |
| T10 Overwhelming HITL | C2 (S, B) |
| T11 Unexpected RCE & Code Attacks | C4 |
| T12 Agent Communication Poisoning | C5 |
| T13 Rogue Agents in MAS | C10 (halt), C9 (detection) |
| T14 Human Attacks on MAS | C1, C5 |
| T15 Human Manipulation | C5, C2 |
| T16 Insecure Inter-Agent Protocol Abuse | C5 (protocol messages and tool metadata as untrusted input), C1 |
| T17 Supply Chain Compromise | C7 |

## What static review can't score
T7 (misaligned/deceptive behaviour) and the model's own refusal behaviour are properties of the model, not the code. This skill credits only deterministic controls that would contain such behaviour (gates, sandboxes, limits, logs). Say so in the report's limitations when it matters.

## Reference designs used to set the top anchors
- **Inspect (UK AISI)** — approval policies where unhandled tool calls are rejected, argument-level matching, decisions approve/modify/reject/escalate/terminate, readable tool views for approvers (C2 L4); tool-result reviewers that run before output reaches the model (C5); Docker/K8s sandboxes (C4); message/token/time/cost limits (C10).
- **Meta, *Agents Rule of Two*** (Oct 2025) — at most two of untrusted input, sensitive access, and state change/external communication per session (C5 S-L3 and B).
- **MCP security best practices** — no token passthrough, per-client consent against confused deputy, consent and sandboxing for local servers (C1 caps, C7).
- **OpenAgentSafety** (ICLR 2026) — real-tool agent evaluations found unsafe behaviour in roughly half to three-quarters of safety-vulnerable tasks across frontier models, including under benign user intent and from non-principal participants; the basis for "prompts are not controls" and principal checks in C2/C5.
