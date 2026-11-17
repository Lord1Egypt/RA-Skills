## Description:

A universal self-improving agent that learns from skill experiences using semantic, episodic, and working memory to propose codebase and skill-guidance improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture lessons from skill executions, extract reusable patterns, and prepare reviewable updates to memory or related skill guidance. It is intended for teams that deliberately want cross-skill learning with human review of proposed changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad cross-skill authority and persistent memory, which can affect unrelated skills if updates are accepted without review.

Mitigation: Use manual invocation or require reviewable diffs before any memory or skill guidance changes are applied.

Risk: The documented global hooks can log raw tool input and output, which may expose sensitive command data or file contents.

Mitigation: Do not enable global hooks unless raw logging is removed or heavily redacted.

Risk: Automatic self-improvement can preserve incorrect or over-generalized lessons as reusable patterns.

Mitigation: Validate proposed patterns against current repository behavior and keep confidence tracking and human feedback in the review loop.

## Reference(s):

- [Appendix](artifact/references/appendix.md)
- [SimpleMem: Efficient Lifelong Memory for LLM Agents](https://arxiv.org/html/2601.02553v1)
- [A Survey on the Memory Mechanism of Large Language Model Agents](https://dl.acm.org/doi/10.1145/3748302)
- [Lifelong Learning of LLM based Agents](https://arxiv.org/html/2501.07278v1)
- [Evo-Memory: DeepMind's Benchmark](https://shothota.medium.com/evo-memory-deepminds-new-benchmark)
- [Let's Build a Self-Improving AI Agent](https://medium.com/@nomannayeem/lets-build-a-self-improving-ai-agent-that-learns-from-your-feedback-722d2ce9c2d9)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON memory patterns, shell hook commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent memory updates, skill edits, and reviewable diffs based on captured execution experience.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
