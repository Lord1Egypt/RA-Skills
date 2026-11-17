## Description:

Uses the Tencent Ads Miaowen AI Q&A API to answer Tencent Ads, WeChat Ads, Moments Ads, Video Accounts Ads, and WeChat Store marketing questions across account setup, qualification review, campaign creation, targeting, bidding, audit rules, creative requirements, reporting, and compliance handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yishuang07](https://clawhub.ai/user/yishuang07)

### License/Terms of Use:

MIT-0

## Use Case:

External users and advertising operators use this skill to ask Tencent Ads business, platform, account, campaign setup, and compliance questions. The skill runs shell scripts that manage a Miaowen API token locally and call Tencent's Miaowen API for answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure from pasting a real Miaowen API token into an AI chat or placing it directly on a command line.

Mitigation: Use a local secret-entry method when possible, prefer least-privilege or revocable tokens, and avoid sharing the full token in chat transcripts, logs, or command history.

Risk: The skill stores the Miaowen access token as plaintext in the user's home directory.

Mitigation: Review the local token file before use, keep permissions restricted to the current user, and rotate or delete the token when it is no longer needed.

Risk: User questions are sent to Tencent's Miaowen API and may contain confidential advertising or business information.

Mitigation: Do not submit sensitive account, customer, campaign, or business data unless the user accepts that it will be sent to Tencent's API.

## Reference(s):

- [Miaowen official site](https://miaowen.qq.com/)
- [Tencent Ads Miaowen chat API endpoint](https://ad.qq.com/ai/gw/ai_customer_service/v1/open_api/chat)
- [ClawHub skill page](https://clawhub.ai/yishuang07/skills/tencentads-miaowen-qa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, a local Miaowen access token, and network access to Tencent's API.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
