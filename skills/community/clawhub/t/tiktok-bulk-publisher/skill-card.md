## Description: <br>
Bulk uploads and publishes TikTok videos with OAuth 2.0 authorization, custom captions, privacy settings, interaction controls, and scheduling options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fly3094](https://clawhub.ai/user/fly3094) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and social media operators can use this skill to automate bulk TikTok video upload, publication, privacy selection, interaction settings, and scheduled posting. It requires TikTok OAuth application credentials before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive TikTok OAuth client credentials. <br>
Mitigation: Use a dedicated TikTok app credential, confirm the requested OAuth scopes, and avoid sharing production credentials with unreviewed automation. <br>
Risk: Bulk or scheduled posting can publish content at scale without enough review safeguards. <br>
Mitigation: Require a dry run or manual approval step before any bulk or scheduled publish. <br>
Risk: The referenced publisher command points to a script that is not included in the artifact. <br>
Mitigation: Inspect the missing publisher script before execution and run the skill only after the implementation is available for review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fly3094/tiktok-bulk-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/fly3094) <br>
- [Provenance](unavailable: No server-resolved GitHub import provenance is stored for this version.) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command examples and credential configuration requirements] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl, TIKTOK_CLIENT_KEY, and TIKTOK_CLIENT_SECRET.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
