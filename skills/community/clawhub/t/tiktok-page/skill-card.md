## Description: <br>
TikTok Page helps an agent manage a TikTok account by posting videos, listing content, checking account stats, refreshing OAuth tokens, and reading comments through TikTok's official API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seph1709](https://clawhub.ai/user/seph1709) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to operate TikTok account workflows such as OAuth setup, account inspection, video listing, publishing, upload status checks, and comment retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use TikTok OAuth credentials to publish videos or read account data for the configured account. <br>
Mitigation: Install only for accounts where agent-assisted management is intended, grant minimal scopes, and confirm the account, file path, caption, privacy level, and upload destination before publishing. <br>
Risk: The local credentials file contains sensitive access, refresh, and client credential material. <br>
Mitigation: Keep ~/.config/tiktok-page/credentials.json out of version control, restrict file permissions, and rotate tokens immediately if exposed or if the host is compromised. <br>
Risk: Expired tokens or missing OAuth scopes can cause failed or partially completed account operations. <br>
Mitigation: Refresh access tokens before calls and re-authorize only with the required TikTok scopes when scope errors occur. <br>


## Reference(s): <br>
- [ClawHub TikTok Page Skill](https://clawhub.ai/seph1709/tiktok-page) <br>
- [TikTok Developers](https://developers.tiktok.com) <br>
- [TikTok Open API Base URL](https://open.tiktokapis.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline PowerShell command examples and API call patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PowerShell or pwsh and a local TikTok OAuth credentials file.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
