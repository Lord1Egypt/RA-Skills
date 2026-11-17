## Description:

Search and browse past conversation history across all sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amor71](https://clawhub.ai/user/amor71)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to find prior OpenClaw conversations, recover decisions or snippets, and resume work that is not captured in memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search private prior OpenClaw conversation transcripts across local agents by default.

Mitigation: Run it only where transcript access is authorized, prefer an explicit --agent scope, and use a narrow --days range for the task.

Risk: Search results and excerpts may expose sensitive conversation content.

Mitigation: Summarize relevant findings instead of copying raw transcript content, and avoid use in shared or multi-user environments unless access boundaries are clear.

## Reference(s):

- [Session History ClawHub page](https://clawhub.ai/amor71/skills/session-history)
- [amor71 publisher profile](https://clawhub.ai/user/amor71)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and summarized search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches local OpenClaw JSONL transcripts and should summarize matches rather than dump raw transcripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
