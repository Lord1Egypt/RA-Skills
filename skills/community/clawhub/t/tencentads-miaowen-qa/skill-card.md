## Description: <br>
Uses Tencent Ads Miaowen's AI Q&A API to answer Tencent Ads, WeChat Ads, Moments Ads, Video Account Ads, and WeChat Store marketing questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yishuang07](https://clawhub.ai/user/yishuang07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, account managers, and agents use this skill to ask Tencent Ads platform questions about account setup, payments, qualifications, campaign creation, targeting, bidding, review rules, materials, reports, and policy issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Miaowen/Tencent Ads API token, and exposing the token could affect the user's account or API access. <br>
Mitigation: Configure the token locally, keep the token file private, avoid sharing the full token in chat or logs, and revoke or delete it when it is no longer needed. <br>
Risk: Questions are sent to the Tencent Ads Miaowen API and may contain sensitive business, campaign, account, or personal information. <br>
Mitigation: Redact confidential details and avoid sending personal data, account secrets, or sensitive business information in prompts. <br>


## Reference(s): <br>
- [Tencent Ads Miaowen](https://miaowen.qq.com/) <br>
- [Tencent Ads Miaowen Chat API](https://ad.qq.com/ai/gw/ai_customer_service/v1/open_api/chat) <br>
- [ClawHub skill page](https://clawhub.ai/yishuang07/tencentads-miaowen-qa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Miaowen API token stored locally before API-backed answers can be retrieved.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
