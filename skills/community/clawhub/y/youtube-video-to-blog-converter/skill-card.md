## Description: <br>
Free basic version that converts YouTube transcript into a structured blog draft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wingogx](https://clawhub.ai/user/wingogx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, marketers, and developers can use this skill to turn a YouTube video title and transcript into a structured markdown blog draft. It supports a free draft workflow and exposes reserved upgrade metadata for future premium publishing features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes payment and upgrade metadata that can route users to a SkillPay endpoint. <br>
Mitigation: Confirm the SkillPay endpoint and fee model before installation, and clearly inform users before any charged workflow is enabled. <br>
Risk: Billing-related data can include user identifiers, wallet details, or sensitive context if callers pass it through metadata. <br>
Mitigation: Keep sensitive conversation content and private business details out of billing metadata. <br>
Risk: Payment integrations may expose API keys or returned credentials if handled carelessly. <br>
Mitigation: Store SkillPay API keys in environment variables and avoid logging secret tokens or returned credentials. <br>


## Reference(s): <br>
- [SkillPay API Contract](references/skillpay-api-contract.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wingogx/youtube-video-to-blog-converter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [JSON result containing a markdown blog draft and upgrade metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user_id, video_title, and transcript; optional video_url and tier affect validation and upgrade messaging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
