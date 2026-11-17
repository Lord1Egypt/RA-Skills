## Description:

Syberz Chatflow Guardian monitors conversation state so agents can keep chats active with timely replies, progress updates, and message completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwwsyber](https://clawhub.ai/user/wwwsyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor supported chat sessions, prevent stalled conversations, send progress updates for long-running work, and configure multi-platform conversation handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and runtime guidance may grant more persistent and sensitive local access than the skill scope clearly explains.

Mitigation: Review scripts before installation, avoid absolute-path /root deployment commands, do not enable the systemd service by default, and prefer a user-level or manual run.

Risk: Local logs may contain private conversation content or recipient identifiers.

Mitigation: Review logging configuration before connecting communication platforms, limit log access, and set retention appropriate for the deployment.

Risk: Dependency provenance should be confirmed before production use.

Mitigation: Regenerate dependencies from a trusted HTTPS registry and run dependency scanning during release validation.

## Reference(s):

- [README](README.md)
- [English README](README_EN.md)
- [Quickstart](QUICKSTART.md)
- [Changelog](CHANGELOG.md)
- [Security Policy](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples plus JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversation monitoring behavior is configurable by interval, response thresholds, quiet hours, platform settings, predictive response options, and deep learning options.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
