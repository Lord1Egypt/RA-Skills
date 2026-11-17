## Description:

Enables an agent to automate Xiaohongshu/RED tasks including searching notes, publishing or deleting posts, retrieving user details, and managing comments.

This skill is for research and development only.

## Publisher:

[osskn4w7](https://clawhub.ai/user/osskn4w7)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill in research or testing workflows to operate a Xiaohongshu account for content discovery, note publication or deletion, user lookup, and comment management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an active Xiaohongshu session cookie that can access account-related data and perform actions.

Mitigation: Use a dedicated or test account where possible, store cookies with restrictive permissions, and rotate or revoke cookies after use.

Risk: The skill can publish, comment, and delete content without strong built-in safeguards.

Mitigation: Require human review and explicit approval before running mutating commands, especially publish, comment, and delete operations.

Risk: Automation can trigger Xiaohongshu risk controls, account restrictions, or bans.

Mitigation: Keep use to research or testing, avoid high-frequency calls, and follow the documented delay guidance between operations.

Risk: The artifact includes a shell=True automation example and dependency installation guidance that can be unsafe if copied directly into production workflows.

Mitigation: Avoid shell=True automation patterns and install pinned dependencies in a virtual environment rather than modifying system Python.

## Reference(s):

- [Xiaohongshu](https://www.xiaohongshu.com)
- [xhs-python-sdk](https://github.com/leeguooooo/xhs-python-sdk)
- [XHS-Downloader](https://github.com/JoeanAmier/XHS-Downloader)
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI text or JSON results, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaohongshu session cookie and can perform account-mutating actions such as publishing, commenting, and deleting content.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog, released 2026-03-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
