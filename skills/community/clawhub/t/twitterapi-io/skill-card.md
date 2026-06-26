## Description: <br>
Interact with Twitter/X through TwitterAPI.io for tweet search, user lookup, posting, likes, retweets, follows, direct messages, webhooks, streams, and related account actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorukardahan](https://clawhub.ai/user/dorukardahan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to have an agent construct TwitterAPI.io requests for reading Twitter/X data and performing authenticated account actions. It is suited for workflows that need endpoint guidance, curl examples, request fields, pagination notes, pricing, and operational caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through live Twitter/X operations with broad account authority. <br>
Mitigation: Require manual confirmation before every post, direct message, follow, delete, upload, profile change, community action, or monitoring rule change. <br>
Risk: The skill requires sensitive credentials such as TwitterAPI.io API keys, login cookies, account credentials, 2FA secrets, and proxy details for write actions. <br>
Mitigation: Use a dedicated or low-risk account, store secrets outside chat and logs, avoid raw shell history exposure, and rotate credentials if they may have been exposed. <br>
Risk: Twitter/X platform behavior and third-party API availability can degrade or change, including documented search pagination and date-range issues. <br>
Mitigation: Validate results before relying on them, use documented timestamp workarounds where applicable, and prefer official Twitter/X APIs for mission-critical posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dorukardahan/twitterapi-io) <br>
- [TwitterAPI.io documentation](https://docs.twitterapi.io) <br>
- [TwitterAPI.io dashboard](https://twitterapi.io/dashboard) <br>
- [Endpoint index](references/endpoint-index.md) <br>
- [Read endpoints](references/read-endpoints.md) <br>
- [Write endpoints](references/write-endpoints.md) <br>
- [Webhook and stream endpoints](references/webhook-stream-endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include API request construction, endpoint selection, pagination handling, authentication setup, and operational warnings.] <br>

## Skill Version(s): <br>
3.8.5 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
