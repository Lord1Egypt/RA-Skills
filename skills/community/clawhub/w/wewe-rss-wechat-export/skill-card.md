## Description:

Exports wewe-rss or JSON Feed style WeChat public account feeds into cleaned DOCX documents with date-prefixed names and optional ZIP packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n1neman](https://clawhub.ai/user/n1neman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to export WeChat public account articles from wewe-rss-compatible feeds into document bundles for review, delivery, or archival workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary feed and image URLs from the agent host.

Mitigation: Run with network controls that block private, link-local, loopback, and metadata-service addresses; only use trusted feed sources.

Risk: The skill writes exported files locally and can process remote content without explicit size limits.

Mitigation: Use a dedicated output directory with disk and memory limits, and review outputs before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/n1neman/skills/wewe-rss-wechat-export)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; generated DOCX, index.txt, and optional ZIP files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports docx and full output modes, dated or plain filenames, and optional ZIP packaging.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
