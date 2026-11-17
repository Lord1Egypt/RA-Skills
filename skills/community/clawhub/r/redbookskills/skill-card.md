## Description:

Publishes image/text or video content to Xiaohongshu (XHS), supports content search and account interactions, and can launch a test browser without publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viv888-ai](https://clawhub.ai/user/viv888-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare, preview, publish, search, and interact with Xiaohongshu content through a controlled browser session. It is intended for workflows that need user confirmation before posting and careful account handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a logged-in Xiaohongshu account, including publishing posts, posting comments, reading notifications and analytics, clearing cookies, and managing persistent Chrome profiles.

Mitigation: Use a test Xiaohongshu account unless those actions are acceptable, require user confirmation before posting, and prefer preview mode for publish workflows.

Risk: Remote CDP browser control can expose an authenticated browser session if used over an untrusted connection.

Mitigation: Keep CDP local or use only a trusted local tunnel, and avoid exposing the debugging port on shared or public networks.

Risk: Security evidence reports an unsafe profile-deletion bug.

Mitigation: Do not use profile deletion until account-name validation and path-containment checks are fixed.

Risk: Publishing from private or internal media URLs may leak content or access patterns to external services.

Mitigation: Use local media files or public media URLs intended for publication, and avoid private or internal URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viv888-ai/skills/redbookskills)
- [README](artifact/README.md)
- [Claude Code integration guide](artifact/docs/claude-code-integration.md)
- [Xiaohongshu](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local title/content files and invoke browser automation scripts when the user confirms an action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
