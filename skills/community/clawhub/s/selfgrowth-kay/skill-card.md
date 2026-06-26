## Description: <br>
A universal self-improving agent that learns from all skill experiences, uses semantic, episodic, and working memory, and supports hooks-based self-correction on skill completion or errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture lessons from agent skill runs, extract reusable patterns, and propose updates to related skills and persistent memory. It is intended for environments where human review can govern automatic hooks and proposed skill changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly observes agent activity and can store persistent memory. <br>
Mitigation: Define redaction, review, retention, and deletion rules before installation, and keep automatic hooks disabled in sensitive projects. <br>
Risk: The skill can propose or make changes to other skills based on learned patterns. <br>
Mitigation: Require visible diffs, human approval, and security review before applying generated skill changes. <br>
Risk: Captured tool inputs or outputs may include project details that should not become long-lived memory. <br>
Mitigation: Limit what hook scripts record and review memory files before sharing, publishing, or reusing them across projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/selfgrowth-kay) <br>
- [Appendix](artifact/references/appendix.md) <br>
- [SimpleMem: Efficient Lifelong Memory for LLM Agents](https://arxiv.org/html/2601.02553v1) <br>
- [A Survey on the Memory Mechanism of Large Language Model Agents](https://dl.acm.org/doi/10.1145/3748302) <br>
- [Lifelong Learning of LLM based Agents](https://arxiv.org/html/2501.07278v1) <br>
- [Evo-Memory: DeepMind's Benchmark](https://shothota.medium.com/evo-memory-deepminds-new-benchmark) <br>
- [Let's Build a Self-Improving AI Agent](https://medium.com/@nomannayeem/lets-build-a-self-improving-ai-agent-that-learns-from-your-feedback-722d2ce9c2d9) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, YAML, shell command, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent memory updates, hook configuration, and skill-file changes that should be reviewed before use.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
