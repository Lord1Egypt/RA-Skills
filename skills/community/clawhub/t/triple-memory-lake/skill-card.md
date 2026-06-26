## Description: <br>
Quad-layer memory system integration - unifies OpenClaw, Claude Code, and self-improving agent memories into a single knowledge lake <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to consolidate Claude Code session logs, OpenClaw daily logs, and self-improving agent metrics into a local memory lake for pattern mining, review, and long-term memory maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy and retain broad private Claude Code session history and OpenClaw agent metrics in a persistent local memory lake. <br>
Mitigation: Run it only when that retention is intended, narrow the source paths before syncing, and delete the memory directory when the history is no longer needed. <br>
Risk: Existing logs may contain secrets or sensitive project information that could be preserved in generated memory and pattern files. <br>
Mitigation: Remove secrets from logs before syncing and inspect generated pattern files before relying on or sharing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hanxiao-bot/triple-memory-lake) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local memory files, indexes, and pattern summaries; no external API output is described.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
