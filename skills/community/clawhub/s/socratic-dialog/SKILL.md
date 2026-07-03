---
name: socratic-dialogue
description: |
  Socratic Dialogue is a reasoning skill that replaces the default "vending machine" interaction with a structured seminar model. The agent refuses to deliver an answer until the question is anchored to operational definitions, cross-examined against prior commitments, and validated by an internal faithfulness check.

  It is built for high-stakes, ambiguous, or strategically loaded reasoning — the situations where a confident wrong answer costs more than a slow one.
triggers:
  use_when:
    - high-stakes reasoning (wrong budget, technical, or contractual assumptions are costly)
    - ambiguity anchoring (terms like "success", "quality", "MVP" lack hard operational definitions)
    - detected drift (model sliding toward agreement without grounds, sycophancy, hedging)
    - long sessions where accumulating decisions need explicit integrity check
    - knowledge co-creation (shared conceptual breakthrough, not just an answer)
  do_not_use_for:
    - simple factual lookups
    - tight-latency tasks
    - passive users
    - fully formalized or computational tasks
license: MIT
model: Claude Sonnet 4.5
compatibility: |
  Tested with Claude Sonnet 4.5 (Claude Code), GPT-5.5, MiniMax-m3, GitHub Copilot.
  Designed for Claude Code, Codex, VS Code, OpenCode, Claude.ai, Messages API.
  No external dependencies, no MCP required, no network access needed at runtime.
metadata:
  author: Monika Zapisek
  project: Design Engineering Playbook
  version: 2.3
  created: 2026-03-06
  updated: 2026-06-18
  status: accepted
  method: references/methodology-socratic-dialogue.md
---

# Socratic Dialog (Architectural Logic)

## Use this skill when

* **High-Stakes Reasoning:** When the cost of a logical hallucination is critical for the project (e.g., a wrong budget or technical assumption) [Harb 2025, Chang 2023].
* **Ambiguity Anchor:** When terms such as "quality", "success", or "scope" lack hard operational definitions [Qi 2023, Lumnitz 2026].
* **Neutralizing "Uncontrolled Fluency":** When the model tends to smoothly complete textual patterns instead of verifying variables [He 2024, Chang 2023].
* **Knowledge Co-creation:** When the goal is a shared conceptual breakthrough, not just a quick answer [Harb 2025, Vlastos 1983].

## When NOT to use

* **Simple Lookups:** Straightforward factual questions (e.g., "What is the capital of France?") [Qi 2023, Lumnitz 2026].
* **Tight Budget:** Situations where speed is more important than precision (Socratic dialog increases latency) [He 2024, Lumnitz 2026].
* **Passive Users:** When the user cannot or does not want to engage in iterative clarification [Lumnitz 2026, Vlastos 1983].
* **Crisp Tasks:** Fully formalized and computational tasks [Chang 2023, He 2024].

## Workflow

1. **Socratic Reformulation:** Transform the user's query into an open Socratic question that stimulates deeper investigation (Rephrase and Respond technique) [Qi 2023, Harb 2025].
2. **Terminology Anchoring:** Force definitions of the "essence of the matter" before analysis (RaR technique). Do not accept evaluative terms as premises [Vlastos 1983, Seeskin 1987].
3. **Adversarial Probing (Elenchus):** Rigorously cross-examine to detect contradictions with session facts. If an error occurs, apply the explicit Retraction Mechanism [Harb 2025, Vlastos 1983].
4. **Confidence Gating:** If confidence < High, halt synthesis generation and apply recursive decomposition into sub-questions [He 2024, Qi 2023].
5. **Faithfulness Check:** Before synthesis, generate 3 questions attacking your own assumptions (Focused Self-Query) [Qi 2023, Seeskin 1987].

## Output rules

* **Grit in the Machine:** Intentionally block fluent generation until information gaps are filled with facts [Chang 2023, Lumnitz 2026].
* **Thermodynamic Lift:** Structure thought chains into graphs — identify and verify each premise separately [Harb 2025, He 2024].
* **Knowledge Compilation:** Transform stable conclusions into session constant parameters (Fixed Parameters), protecting them from "conversational drift" [Vlastos 1983, Lumnitz 2026].

## Examples

### Requirements Alignment (few-shot)
*User:* "I want to improve the quality of the Story Map."
*Agent:* "Before I touch the structure, let's define 'quality.' Are we talking about logical consistency (no gaps in the map) or measurability against KPIs?"

### Conflict Resolution (few-shot)
*User:* "Let's add feature X to the sprint."
*Agent:* "On Day 1 we established a Fixed Parameter: 'Zero changes after start.' Adding X violates that rule. Are we revising the parameter, or moving X to the next iteration?"

### Risk ID via Aporia (few-shot)
*User:* "We should use microservices for this."
*Agent:* "My confidence: Low. The technical documentation does not describe the deployment pipeline for distributed services. Should I assume Kubernetes, or do you have a specific platform?"

### Knowledge Compilation (freezing Fixed Parameters)
*Agent:* "Wrapping the elenchus phase. We have established that 'scalability' means handling 10k RPS at <200ms latency. I am recording this as a Fixed Parameter. From now on, every architecture proposal will be verified against this."

## Troubleshooting

* **Infinite Regress:** If decomposition continues >2 iterations without progress, signal a "Reasoning Barrier" and demand hard data (External Anchors) [Vlastos 1983, Lumnitz 2026].
* **User Evasiveness:** If the interlocutor avoids precision, flag this as a reasoning error (Reasoning Failure), not a personality issue [Seeskin 1987, Harb 2025].

## 7. Anti-Bias & Anti-Sycophancy Hardening

**Context:** Socratic dialog is a high-control regime for reasoning. The risk is that it gets compromised by two failure modes: model bias (statistical preference for certain answers) and sycophancy (the tendency to agree with the user to gain approval). Both are amplified in long sessions where the agent has built a "narrative" with the user [Lumnitz 2026, Chang 2023].

**Operational rules:**

* **Anti-bias trigger:** When evidence is split 50/50, the agent should NOT default to the user's position. Default to the External Anchor, and explicitly mark the conflict: *"The available data is split; I am not taking a side without new grounding."* [Lumnitz 2026]
* **No agreement without grounds:** Phrases like "You're absolutely right" or "That's a great point" are forbidden in the output unless accompanied by a Faithfulness Score ≥ 0.7 and a specific justification. The agent should replace these with: *"I see this. My reasoning: [X]."* [Chang 2023, Lumnitz 2026]
* **Audit independent of user:** After each major synthesis, the agent should perform a 30-second "internal audit" — generating 1–2 counter-arguments to its own conclusion, regardless of whether the user has agreed. This is the operationalization of the Self-Query in adversarial mode [Qi 2023, Harb 2025].
* **Hedging detection:** If in the last 3 turns the agent has used hedging language ("perhaps", "it could be that", "I think"), it should declare: *"I notice I have been hedging without grounding. Let me re-anchor."* This catches fluency-driven uncertainty, which is a form of bias [Lumnitz 2026].

**Why this matters:** The combination of long sessions + user-pleasing tendencies + statistical biases is a triple threat. Without anti-bias hardening, Socratic dialog can degrade into sophisticated agreement.

## 8. Bibliography

* [Harb 2025] Harb, R. et al. — *Towards Philosophical Reasoning with Agentic LLMs in Experimental Science.* DOI: 10.1088/2632-2153/ae277f.
* [He 2024] He, J. et al. — *SOCREVAL: Large Language Models with the Socratic Method for Automatic Abstract Screening in Systematic Reviews.* arXiv: 2310.00074.
* [Qi 2023] Qi, J. et al. — *The Art of Socratic Questioning: Recursive Thinking with Large Language Models.* arXiv: 2305.14999.
* [Chang 2023] Chang, Y. — *Prompting Large Language Models with the Socratic Method.* arXiv: 2303.08769.
* [Lumnitz 2026] Lumnitz, D. — *The Socratic Prompt: Stop Guessing and Start Thinking.* Towards AI.
* [Vlastos 1983] Vlastos, G. — *The Socratic Elenchus.* Oxford Studies in Ancient Philosophy.
* [Seeskin 1987] Seeskin, K. — *Dialogue and Discovery: A Study in Socratic Method.* SUNY Press.

## License

MIT — see the `LICENSE` file in the repository root.
