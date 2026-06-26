## Description: <br>
Optimizes OpenClaw token usage with context compression, semantic deduplication, and adaptive token budgeting to reduce API cost and memory footprint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akanji-creator](https://clawhub.ai/user/akanji-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to analyze, compress, and optimize long-running agent conversations before model calls. It is aimed at reducing token usage, latency, memory footprint, and API costs while preserving useful recent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect and rewrite conversation context before model calls. <br>
Mitigation: Avoid automatic mode for secrets, regulated data, legal, medical, security, or exact-fidelity workflows; review optimized context behavior before deployment. <br>
Risk: Default session handling and session-file selection may expose unintended local conversation data. <br>
Mitigation: Use explicit session files, validate session paths, and document privacy, caching, checkpointing, and disable controls before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/akanji-creator/turboquant-optimizer) <br>
- [TurboQuant research article](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Training documentation](artifact/docs/TRAINING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples, plus JSON configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces token-optimization statistics and may rewrite conversation context before model calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
