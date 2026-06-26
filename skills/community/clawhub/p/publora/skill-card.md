## Description: <br>
Publora API helps agents schedule, publish, draft, bulk-schedule, and manage social media posts across supported platforms through Publora. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and workspace operators use this skill to guide agents through Publora API workflows for creating posts, scheduling content, uploading media, configuring webhooks, managing workspace users, and retrieving LinkedIn analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Publora API key can publish, schedule, delete posts, upload media, configure webhooks, and act for workspace users. <br>
Mitigation: Use least-privilege handling for API keys, never expose workspace keys client-side, and require explicit confirmation before live posts, deletions, media uploads, webhook changes, or workspace-user actions. <br>
Risk: Draft-versus-publish behavior is ambiguous in the artifact and could affect real social accounts. <br>
Mitigation: Verify Publora's current draft and immediate publishing behavior before use, and treat omitted scheduling fields as requiring explicit user confirmation. <br>
Risk: Webhook configuration can send publishing, failure, and token-expiration events to external endpoints. <br>
Mitigation: Configure webhooks only to endpoints the operator controls, save and verify webhook secrets, and rotate secrets when endpoint ownership or access changes. <br>


## Reference(s): <br>
- [Publora skill page](https://clawhub.ai/sergebulaev/publora) <br>
- [Publora API Docs](https://github.com/publora/publora-api-docs) <br>
- [Publora Pricing](https://publora.com/pricing) <br>
- [Publora API base URL](https://api.publora.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript, Python, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API endpoint paths, request headers, JSON payload examples, webhook setup steps, and platform limit guidance.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
