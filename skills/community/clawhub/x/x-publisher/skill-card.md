## Description: <br>
Publish tweets to X (Twitter) using the official Tweepy library, including text-only tweets, tweets with images or videos, and detailed publish results with tweet ID and URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manifoldor](https://clawhub.ai/user/manifoldor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to verify X API credentials and publish prepared text or media posts from a configured X account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses API credentials that can post from the configured X account. <br>
Mitigation: Use a dedicated account or least-privilege tokens when possible, store credentials only in protected environment variables, and rotate tokens if they may have been exposed. <br>
Risk: The tweet command can publish unintended text or media to a public account. <br>
Mitigation: Review the tweet text and every media path before running the command, and verify credentials against the intended account before publishing. <br>


## Reference(s): <br>
- [X API Reference](references/x_api.md) <br>
- [Tweepy Documentation](https://docs.tweepy.org/) <br>
- [X API Documentation](https://developer.twitter.com/en/docs/twitter-api) <br>
- [X Developer Portal](https://developer.twitter.com/en/portal/dashboard) <br>
- [ClawHub Skill Listing](https://clawhub.ai/manifoldor/x-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [CLI output with optional JSON publish result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can publish public X posts and selected media from the configured account after credentials are provided.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
