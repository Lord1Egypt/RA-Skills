## Description:

Summarizes recent posts from followed Knowledge Planet circles into a daily or per-circle digest using a local session token, with browser-assisted recovery when token mode is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sealiu1997](https://clawhub.ai/user/sealiu1997)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to collect recent visible Knowledge Planet updates from followed circles, deduplicate them, and generate a concise digest for deciding which posts to read first. It is intended for private membership content where session tokens and captured cookies remain local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Knowledge Planet session cookies and token files that could expose account access if copied into logs, shared screenshots, repositories, or public artifacts.

Mitigation: Use it only in a private local environment, keep state/session.token.json and captured cookie files under gitignored local paths, and avoid sharing tool logs that may contain credential material.

Risk: Probe or custom API-base options can send authenticated requests outside the intended Knowledge Planet endpoint if pointed at untrusted URLs.

Mitigation: Use the default trusted endpoint for normal runs and avoid probe or custom API-base options with untrusted URLs.

Risk: Token, browser, or fetch-based collection can fail, expire, or capture incomplete private-member content.

Mitigation: Validate authentication before extraction, return explicit failure states such as TOKEN_EXPIRED or PARTIAL_CAPTURE, preserve original links, and do not fabricate missing summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sealiu1997/skills/zsxq-digest)
- [README](README.md)
- [Runtime modes](references/runtime-modes.md)
- [Session token guide](references/session-token-guide.md)
- [Output schema](references/output-schema.md)
- [Browser recovery](references/browser-recovery.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown digest with JSON collection and state files, plus shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Digest items can include circle name, author, timestamp, content preview, priority, suggested action, original URL, and partial-capture status when extraction is incomplete.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
