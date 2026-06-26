## Description: <br>
Compress conversation context into a TurboQuant vector store inside OpenClaw memory, then retrieve the most relevant entries on demand to stay within token budgets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twacqwq](https://clawhub.ai/user/twacqwq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to persist compressed conversation context, retrieve relevant prior messages for prompts, and compact stored entries when memory grows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local memory store may retain sensitive conversation text across turns or session restarts. <br>
Mitigation: Avoid ingesting secrets or confidential material, and periodically inspect or clear ~/.openclaw/memory. <br>
Risk: Compaction deletes stored context entries and may remove information needed later. <br>
Mitigation: Treat compact operations as deletion, choose retention thresholds deliberately, and verify retrieved context before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twacqwq/turboquant) <br>
- [OpenClaw TurboQuant homepage](https://github.com/openclaw/openclaw-turboquant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON command-output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires caller-provided .npy embedding vectors, uv on PATH, and a local OpenClaw memory store.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
