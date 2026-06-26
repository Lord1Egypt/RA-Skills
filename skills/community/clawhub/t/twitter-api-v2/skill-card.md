## Description: <br>
Access X (Twitter) via API v2: user profiles, timelines, threads, search, bookmarks, likes, and posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve X user profiles, timelines, recent search results, threads, bookmarks, liked tweets, and tweet details, and to post tweets when OAuth is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use X API credentials and OAuth tokens, including permissions for bookmarks, likes, and posting. <br>
Mitigation: Use bearer-token mode for read-only public lookups when possible, enable OAuth only when those user-context actions are needed, and protect local credential files with restrictive permissions. <br>
Risk: Posting through OAuth can publish content to an X account. <br>
Mitigation: Review exact tweet text before posting and keep OAuth app scopes limited to the documented needs. <br>
Risk: X API requests can incur usage charges and still remain subject to rate limits. <br>
Mitigation: Set X API spending limits, monitor API usage, and keep request sizes and retry behavior conservative. <br>


## Reference(s): <br>
- [X API Setup Guide](SETUP.md) <br>
- [X API Quick Reference](references/quickstart.md) <br>
- [X API Pricing](references/pricing.md) <br>
- [ClawHub skill page](https://clawhub.ai/odrobnik/twitter-api-v2) <br>
- [Publisher profile](https://clawhub.ai/user/odrobnik) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and X API credentials; OAuth is needed for bookmarks, likes, and posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
