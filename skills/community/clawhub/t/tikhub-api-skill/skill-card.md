## Description: <br>
Search and query TikHub API endpoints for TikTok, Douyin, Xiaohongshu, Lemon8, Instagram, YouTube, Twitter, Reddit, and other social media platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangdabiao](https://clawhub.ai/user/liangdabiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to discover TikHub API endpoints, identify required parameters, and make requests for social media data retrieval workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence flags unsafe token handling, and the client includes a default bearer token. <br>
Mitigation: Replace the default token with a scoped secret supplied through the environment and rotate any exposed token before use. <br>
Risk: The release evidence flags under-disclosed login, account-action, cookie/proxy, disposable-email, metric-manipulation, and view-count capabilities. <br>
Mitigation: Limit use to explicitly intended endpoints, confirm platform-rule compliance, and avoid high-risk workflows unless they are approved for the deployment. <br>
Risk: The skill can make outbound API requests based on user-provided paths and parameters. <br>
Mitigation: Restrict requests to TikHub domains, review request parameters before execution, and avoid sending sensitive or unnecessary data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liangdabiao/tikhub-api-skill) <br>
- [TikHub API documentation](https://api.tikhub.io) <br>
- [TikHub Apifox documentation](https://docs.tikhub.io) <br>
- [TikHub API status](https://monitor.tikhub.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include endpoint paths, required parameters, request examples, and formatted API response summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
