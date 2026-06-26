## Description: <br>
Get trending topics on X (Twitter) using the X API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terryds](https://clawhub.ai/user/terryds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch current X trending topics for a WOEID location and to look up WOEID values for cities or countries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a user-provided X API bearer token. <br>
Mitigation: Use a minimally scoped token where possible, keep it private, and revoke it from the X Developer Portal when the skill is no longer used. <br>


## Reference(s): <br>
- [X Developer Portal](https://developer.x.com) <br>
- [X API trends endpoint](https://api.x.com/2/trends/by/woeid/1?trend.fields=trend_name,tweet_count) <br>
- [ClawHub skill page](https://clawhub.ai/terryds/x-trends-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scripts emit JSON trend and WOEID lookup results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and X_BEARER_TOKEN; trend results include names and tweet counts when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
