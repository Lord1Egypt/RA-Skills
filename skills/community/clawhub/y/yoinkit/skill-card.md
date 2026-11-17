## Description:

Search, analyze, and transcribe content across 13 social platforms — trending topics, video transcripts, post metadata, and multi-platform research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seomikewaltman](https://clawhub.ai/user/seomikewaltman)

### License/Terms of Use:

MIT

## Use Case:

External users and content researchers use YoinkIt to gather social post metadata, video transcripts, creator feeds, trending topics, and multi-platform research results through OpenClaw commands and scheduled workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends social URLs, handles, search topics, transcripts, and related metadata to Yoinkit through a configurable remote endpoint.

Mitigation: Install only when that data sharing is acceptable, keep YOINKIT_API_URL on the default HTTPS Yoinkit endpoint unless using a trusted local server, and use a separate development token for local testing.

Risk: Optional cron examples can run recurring research workflows and some Obsidian examples overwrite notes.

Mitigation: Review scheduled workflow examples before enabling them, especially Obsidian jobs that update existing files.

Risk: The release security verdict requires review and notes response branding behavior.

Mitigation: Review and scan the skill before deployment, and confirm output branding behavior is appropriate for the target agent environment.

## Reference(s):

- [Yoinkit Platform Capabilities](references/platforms.md)
- [Yoinkit API Endpoint](https://yoinkit.ai/api/v1/openclaw)
- [Yoinkit](https://yoinkit.ai)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON from API wrapper commands, plus human-facing Markdown summaries and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Yoinkit API token; optional scheduled workflows can produce recurring research notes and alerts.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
