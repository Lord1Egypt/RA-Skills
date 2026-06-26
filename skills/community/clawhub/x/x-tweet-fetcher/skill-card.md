## Description: <br>
Fetches public X/Twitter tweets without login or API keys, including regular tweets, long tweets, quoted tweets, and full X Articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjw21century](https://clawhub.ai/user/hjw21century) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to retrieve public X/Twitter post content, engagement stats, quoted tweets, and long-form X Articles from a tweet URL without account credentials or API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tweet lookup requests are sent to FxTwitter, which may observe requested tweet IDs and request metadata. <br>
Mitigation: Avoid using the skill for sensitive URLs, and review FxTwitter privacy and provider suitability before deployment. <br>
Risk: The skill depends on FxTwitter availability and cannot fetch deleted, private, or reply-thread content. <br>
Mitigation: Handle fetch errors explicitly and use a fallback process when content is unavailable or reply text is required. <br>


## Reference(s): <br>
- [FxTwitter](https://github.com/FxEmbed/FxEmbed) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/hjw21century/x-tweet-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [JSON object or plain text from a Python CLI/API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes tweet text, article text, author metadata, engagement counts, quote data, and error messages when fetching fails.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
