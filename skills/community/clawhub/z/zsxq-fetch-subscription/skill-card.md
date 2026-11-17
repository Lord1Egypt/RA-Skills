## Description:

Use this skill when the user wants OpenClaw to query synced Zhishi Xingqiu content, inspect recent posts, search downloaded documents, summarize updates, or answer questions grounded in the local ZSXQ database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hashedalex](https://clawhub.ai/user/hashedalex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect synced ZSXQ group content, summarize recent updates, search downloaded documents, and answer questions from local database records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented server startup can expose private synced content and sync controls on all network interfaces without documented authentication.

Mitigation: Keep port 8000 private, prefer binding the service to 127.0.0.1, add authentication where possible, and approve manual syncs only when fresh external content is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hashedalex/skills/zsxq-fetch-subscription)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown or text with inline shell commands and endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should be grounded in retrieved local ZSXQ records and cite the topic text or document preview used when available.]

## Skill Version(s):

1.0.0 (source: server release evidence and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
