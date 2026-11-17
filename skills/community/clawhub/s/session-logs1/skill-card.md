## Description:

Search and analyze your own session logs (older/parent conversations) using jq.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanjiang8124](https://clawhub.ai/user/yanjiang8124)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to locate, filter, and summarize older OpenClaw session transcripts when prior conversation context is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad searches across all session transcripts can expose unrelated private conversations, secrets, personal information, customer data, or unrelated private work.

Mitigation: Scope use to a specific session, date, keyword, or transcript before searching, and review excerpts before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanjiang8124/skills/session-logs1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local access to OpenClaw session JSONL files and the jq and rg command-line tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
