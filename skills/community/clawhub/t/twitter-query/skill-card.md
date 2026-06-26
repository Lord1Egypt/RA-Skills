## Description: <br>
Query X/Twitter via twitterapi.io read-only APIs by account timeline or keyword search, returning structured JSON without bundled LLM summarization or trend scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexander10011](https://clawhub.ai/user/alexander10011) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to retrieve recent tweets from a handle or run advanced X/Twitter keyword, hashtag, or cashtag searches through twitterapi.io. It is useful when an agent needs read-only tweet data as JSON for downstream inspection or summarization in the current conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user-provided API key, search queries, and requested usernames to twitterapi.io, or to a replacement endpoint if TWITTER_API_BASE is changed. <br>
Mitigation: Install only if you are comfortable using twitterapi.io, keep TWITTER_API_BASE unset unless you trust the replacement endpoint, and manage TWITTER_API_KEY as a secret. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alexander10011/twitter-query) <br>
- [twitterapi.io Documentation](https://docs.twitterapi.io/introduction) <br>
- [twitterapi.io User Last Tweets Endpoint](https://docs.twitterapi.io/api-reference/endpoint/get_user_last_tweets) <br>
- [twitterapi.io Advanced Search Endpoint](https://docs.twitterapi.io/api-reference/endpoint/tweet_advanced_search) <br>
- [Twitter Advanced Search Syntax Reference](https://github.com/igorbrigadir/twitter-advanced-search) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON printed to stdout, with command guidance in Markdown documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TWITTER_API_KEY; TWITTER_API_BASE is optional and defaults to https://api.twitterapi.io.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
