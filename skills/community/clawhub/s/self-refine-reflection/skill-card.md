## Description:

Adds an internal self-review loop that helps an agent critique and refine responses before delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT

## Use Case:

Agents and their users use this skill to add a pre-delivery self-review loop that checks responses for logic, factual accuracy, completeness, conciseness, actionability, and consistency. It is especially aimed at developers and engineers who need precise, actionable AI responses with less follow-up correction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent reflection notes can retain sensitive project or user information across sessions.

Mitigation: Disable or remove the memory/reflections.md behavior for sensitive work, or restrict the skill to in-conversation memory and periodically review or delete stored notes.

Risk: The skill broadly changes agent behavior by adding self-review before final responses.

Mitigation: Enable it only where an agent-wide self-review layer is desired, and prefer project-scoped installation when global behavior changes are not acceptable.

Risk: Self-review can still miss factual errors or reinforce an incorrect assumption.

Mitigation: Use external verification and human review for factual, high-stakes, or security-sensitive claims before acting on the refined response.

## Reference(s):

- [Benchmark Report](BENCHMARK.md)
- [Academic Sources](references/sources.md)
- [Reflection Prompt Templates](references/reflection-templates.md)
- [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
- [Chain-of-Verification Reduces Hallucination in Large Language Models](https://arxiv.org/abs/2309.11495)
- [Language Models (Mostly) Know What They Know](https://arxiv.org/abs/2207.05221)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code blocks, shell command blocks, and reflection notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent reflection notes when file-backed memory is available; otherwise stores notes only in conversation context.]

## Skill Version(s):

2.0.1 (source: ClawHub release metadata; artifact changelog top entry is 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
