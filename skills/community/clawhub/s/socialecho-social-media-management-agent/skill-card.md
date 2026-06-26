## Description: <br>
SocialEcho social media management API skill for querying team, accounts, articles, reports, upload URL, Reddit communities, Pinterest boards, and publishing posts using team API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[socialecho-net](https://clawhub.ai/user/socialecho-net) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and social media teams use this skill to inspect SocialEcho team data, accounts, articles, reports, upload URLs, Reddit communities, Pinterest boards, and to publish or schedule posts through SocialEcho APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live social media posts through SocialEcho. <br>
Mitigation: Require human review for publish payloads, especially payloads that set status to 1. <br>
Risk: The SocialEcho team API key can be sent to a user-specified API host. <br>
Mitigation: Use the default SocialEcho API host when possible and avoid non-HTTPS or untrusted --base-url values. <br>
Risk: The skill requires sensitive SocialEcho credentials. <br>
Mitigation: Use a least-privilege team API key and install only when the agent is intended to operate SocialEcho accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/socialecho-net/socialecho-social-media-management-agent) <br>
- [Publisher profile](https://clawhub.ai/user/socialecho-net) <br>
- [SocialEcho app](https://app.socialecho.net/) <br>
- [SocialEcho API base](https://api.socialecho.net) <br>
- [OpenAPI specification](artifact/openapi.yaml) <br>
- [Platform publish limits](artifact/platform-publish-limits_en.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Markdown, Guidance] <br>
**Output Format:** [JSON API responses, command-line output, and Markdown reference text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SocialEcho team API key; publish payloads can create drafts, scheduled posts, or live posts depending on status.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
