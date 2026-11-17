## Description:

TikTok manager: post videos, list content and check account stats using TikTok API calls from PowerShell or pwsh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seph1709](https://clawhub.ai/user/seph1709)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage a TikTok account from an agent session: guide OAuth setup, refresh tokens, read account and video data, list comments, upload videos, publish videos, and check publish status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived TikTok credentials are stored in a local plaintext file.

Mitigation: Use owner-only permissions for ~/.config/tiktok-page/credentials.json, avoid shared machines, and revoke or rotate tokens immediately if the host or file may have been exposed.

Risk: The skill can publish videos publicly or with account-impacting privacy settings.

Mitigation: Confirm the target account, video, caption, OAuth scopes, and privacy level before running publish or upload actions.

Risk: OAuth scopes may grant access to account data, video lists, publishing, uploads, and comments.

Mitigation: Grant only the minimum TikTok scopes needed for the intended workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seph1709/skills/tiktok-page)
- [TikTok Developer Portal](https://developers.tiktok.com)
- [TikTok API Base URL](https://open.tiktokapis.com/v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline PowerShell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include TikTok API request snippets, setup steps, token refresh guidance, parsed API responses, and error-specific remediation.]

## Skill Version(s):

1.0.4 (source: artifact/_meta.json and evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
