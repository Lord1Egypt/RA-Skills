## Description:

Xiaohongshu Skill helps agents use a Python Playwright CLI to search and read Xiaohongshu content, manage login sessions, publish posts, comment, like, and collect content while requiring explicit confirmation for account-changing actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deliciousbuding](https://clawhub.ai/user/deliciousbuding)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent operators use this skill to automate Xiaohongshu research, content preparation, publishing, comments, likes, collections, and account-session workflows through a JSON-oriented CLI. It is intended for controlled use with explicit human approval before actions that affect a real account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, comment, like, collect, and otherwise change a real Xiaohongshu account.

Mitigation: Use a dedicated account where possible and require explicit human confirmation before every public post, comment, like, collect, or account-state change.

Risk: Local browser state and Xiaohongshu session data may expose account access or private account information.

Mitigation: Keep ~/.xiaohongshu private, do not share browser profile files or QR codes, and avoid attaching account data or complete security parameters to issues or logs.

Risk: The security scan notes under-scoped local deletion and silent browser-script override behavior.

Mitigation: Review the installed source before use, prefer ClawHub or another pinned and reviewed source, check that ~/.xiaohongshu/stealth.js is absent or intentionally trusted, and avoid passing arbitrary paths to --cookie during logout.

Risk: Unconfirmed submissions or repeated automation can create unintended duplicate or policy-sensitive platform actions.

Mitigation: Manually review submitted_unconfirmed results, do not automatically retry writes, and consider Xiaohongshu platform rules for browser automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deliciousbuding/skills/xiaohongshu-skill)
- [Publisher Profile](https://clawhub.ai/user/deliciousbuding)
- [CLI API](docs/API.md)
- [Installation](docs/INSTALL.md)
- [Security](docs/SECURITY.md)
- [Integrations](docs/INTEGRATIONS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require explicit user confirmation; command diagnostics are emitted separately from JSON results.]

## Skill Version(s):

1.5.1 (source: server release, pyproject.toml, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
