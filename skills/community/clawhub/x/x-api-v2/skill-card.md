## Description: <br>
Access X (Twitter) via API v2 for user profiles, timelines, threads, search, bookmarks, likes, and posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query X API v2 for public account and post data, extract recent threads and search results, and perform OAuth-authorized user actions such as reading bookmarks or posting tweets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth mode can read private account data and post publicly from the user's X account. <br>
Mitigation: Use bearer-token mode for public read-only lookups, enable OAuth only when bookmarks, likes, or posting are required, and require explicit approval before posting. <br>
Risk: Stored X API credentials and OAuth tokens can grant account access if exposed. <br>
Mitigation: Protect ~/.openclaw/x with restrictive permissions and avoid sharing credential or token files. <br>
Risk: X API usage can incur charges and rate limits. <br>
Mitigation: Set X API spending limits, monitor usage, cache results when appropriate, and design workflows to respect rate limits. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/odrobnik/x-api-v2) <br>
- [X API setup guide](SETUP.md) <br>
- [X API pricing reference](references/pricing.md) <br>
- [X API quick reference](references/quickstart.md) <br>
- [X Developer Platform](https://developer.x.com) <br>
- [X Developer Portal](https://developer.x.com/en/portal/projects-and-apps) <br>
- [X API usage endpoint](https://api.x.com/2/usage/tweets) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and X API credentials; OAuth mode enables private data access and posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
