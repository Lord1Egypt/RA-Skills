## Description: <br>
Monitor specific X/Twitter accounts and surface noteworthy tweets on a configurable schedule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vmathur](https://clawhub.ai/user/vmathur) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users monitor a configured list of X/Twitter accounts for high-value technology and trend posts, then receive scheduled or manual summaries filtered against their criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an X API bearer token for scheduled polling. <br>
Mitigation: Use a limited token where possible, restrict permissions on credentials.json, and keep it out of version control and backups. <br>
Risk: Fetched tweet text is retained in a local history file. <br>
Mitigation: Delete tweet_history.json periodically if a retained local archive is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vmathur/x-monitor) <br>
- [X API recent search endpoint](https://api.x.com/2/tweets/search/recent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON-backed tweet data and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured handles, schedule, timezone, API credentials, and noteworthy criteria.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
