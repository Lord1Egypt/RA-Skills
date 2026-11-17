## Description:

Converts webpages, especially WeChat articles, into offline-readable PDF and Markdown files while preserving images, layout, and styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinkaizhou](https://clawhub.ai/user/qinkaizhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-operations users use this skill to archive single webpages or batches of URLs as local PDF and Markdown documents for offline reading and recordkeeping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default browser mode reuses the user's Chrome profile and can expose cookies or logged-in sessions.

Mitigation: Prefer --isolated or HTTP mode for public content; use a disposable browser profile, VM, or sandbox when login-required pages must be archived.

Risk: The local CDP proxy opens a localhost port and may leave temporary state files.

Mitigation: Validate input URLs before use, stop the proxy after the task, and clean cdp-proxy state files from the temp directory if cleanup does not complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qinkaizhou/skills/url2pdf-mk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime output is local PDF and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser mode can access logged-in sessions; HTTP mode produces Markdown only.]

## Skill Version(s):

1.1.1 (source: server release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
