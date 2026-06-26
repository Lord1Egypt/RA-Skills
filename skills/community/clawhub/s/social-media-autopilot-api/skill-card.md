## Description: <br>
SocialEcho social media management API skill for querying team, accounts, articles, reports, upload URL, Reddit communities, Pinterest boards, and publishing posts using a team API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[socialecho-net](https://clawhub.ai/user/socialecho-net) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social media operations teams use this skill to query SocialEcho team, account, article, reporting, upload, Reddit, Pinterest, and publishing endpoints from an agent workflow using an explicit team API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SocialEcho team API key that can access team data and publishing endpoints. <br>
Mitigation: Use a least-privilege or revocable API key and avoid exposing the key in shared command logs or prompts. <br>
Risk: Publishing commands can create or schedule external social media posts. <br>
Mitigation: Review publish payloads, account IDs, status values, scheduled times, and platform publish limits before running publish commands. <br>
Risk: The optional base URL setting can direct requests to an unintended endpoint. <br>
Mitigation: Confirm the base URL before execution and use the default SocialEcho API endpoint unless an approved alternative is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/socialecho-net/social-media-autopilot-api) <br>
- [SocialEcho Publisher Profile](https://clawhub.ai/user/socialecho-net) <br>
- [OpenAPI Definition](artifact/openapi.yaml) <br>
- [Platform Publish Limits](artifact/platform-publish-limits_en.md) <br>
- [SocialEcho Application](https://app.socialecho.net/) <br>
- [SocialEcho API Base URL](https://api.socialecho.net) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown guidance] <br>
**Output Format:** [JSON API responses and Markdown guidance with CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an explicit team API key; supports optional base URL, team ID, and language parameters.] <br>

## Skill Version(s): <br>
1.3.0 (source: server evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
