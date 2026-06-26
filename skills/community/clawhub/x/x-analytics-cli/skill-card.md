## Description: <br>
X Analytics CLI helps agents retrieve and analyze X (Twitter) data with x-analytics-cli, including tweet search, tweet counts, user profiles, tweet lookup, and timelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to run read-only X API v2 analytics through the x-analytics-cli, including recent tweet search, tweet count trends, user and tweet lookup, and authenticated timeline retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires X API OAuth credentials and sends searches, usernames, tweet IDs, and authenticated timeline or profile requests to X through the CLI. <br>
Mitigation: Use least-privilege or low-risk OAuth tokens where possible, keep credentials out of chat and logs, and confirm the user expects the requested data to be sent to X. <br>
Risk: Some commands depend on X API access tier, rate limits, token validity, and endpoint availability. <br>
Mitigation: Verify credentials with x-analytics-cli me, handle authorization, forbidden, empty-result, and rate-limit errors explicitly, and explain access-tier limits before retrying. <br>


## Reference(s): <br>
- [x-analytics-cli documentation](https://github.com/Bin-Huang/x-analytics-cli) <br>
- [X API v2 overview](https://docs.x.com/x-api) <br>
- [X API Tweet Lookup](https://docs.x.com/x-api/posts/lookup) <br>
- [X API User Lookup](https://docs.x.com/x-api/users/lookup) <br>
- [X API Recent Search](https://docs.x.com/x-api/posts/search) <br>
- [X API Tweet Counts](https://docs.x.com/x-api/posts/counts) <br>
- [X API Timelines](https://docs.x.com/x-api/posts/timelines) <br>
- [X API Fields and Expansions](https://docs.x.com/x-api/fields) <br>
- [X API Search Query Syntax](https://docs.x.com/x-api/posts/search/integrate/build-a-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying CLI returns JSON responses and JSON-formatted errors from X API v2 requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
