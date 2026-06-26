## Description: <br>
Provides OAuth 1.0a access to X API v2 for posting tweets, creating threads, deleting tweets, checking account info, and retrieving mentions or search results when the account tier permits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngmeyer](https://clawhub.ai/user/ngmeyer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent operate an X account through official OAuth credentials for posting, threads, deletion, account checks, mentions, and search. It is intended for accounts where the operator is comfortable granting write authority and reviewing public actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post or delete content from a live X account using OAuth credentials. <br>
Mitigation: Require explicit human review before posts, threads, or deletions, and verify tweet IDs before deletion. <br>
Risk: Declared scope conflicts with implemented search and mentions features, and those endpoints may require a paid X API tier. <br>
Mitigation: Treat search and mentions as available capabilities, check the account tier before use, and expect clear failure handling on unsupported tiers. <br>
Risk: The automation template can publish unattended public posts if configured and scheduled. <br>
Mitigation: Use the automation template only when unattended posting is intentional, customize content deliberately, and keep daily limits and cooldowns enabled. <br>
Risk: OAuth credentials grant account authority and can fail after rotation or if copied with extra whitespace. <br>
Mitigation: Store credentials securely, rotate all four OAuth values together, and validate copied values before use. <br>


## Reference(s): <br>
- [ClawHub listing for X OAuth API](https://clawhub.ai/ngmeyer/x-oauth-api) <br>
- [X Developer Platform](https://developer.twitter.com/) <br>
- [X API rate limits](https://developer.twitter.com/en/docs/twitter-api/rate-limits) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and JSON from CLI commands, with Markdown guidance when used by an agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X OAuth environment variables and network access to api.twitter.com; some commands depend on paid X API tiers.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
