## Description: <br>
X Research searches X/Twitter for recent perspectives, developer discussions, product feedback, cultural takes, breaking news, and expert opinions, then helps agents synthesize sourced briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aviclaw](https://clawhub.ai/user/aviclaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and other external agent users use this skill to search recent X/Twitter discourse, inspect profiles, follow threads, monitor watchlists, and turn the findings into concise sourced research notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an X API bearer token and may incur paid API reads. <br>
Mitigation: Use a token scoped for this purpose, monitor X API spending, and use quick mode, caching, and spending controls for cost management. <br>
Risk: Sensitive research topics may leave local cache entries, watchlists, or saved drafts. <br>
Mitigation: Clear cache and drafts after sensitive work, and avoid storing unrelated secrets in the same global environment file. <br>
Risk: Heartbeat watchlist checks can repeatedly query watched accounts and consume API credits. <br>
Mitigation: Enable watchlist checks only intentionally and keep monitored accounts focused on actionable use cases. <br>


## Reference(s): <br>
- [ClawHub X Research Release](https://clawhub.ai/aviclaw/x-research) <br>
- [X API Reference](references/x-api.md) <br>
- [X Developer Portal](https://developer.x.com) <br>
- [X Developer Console](https://console.x.com) <br>
- [X API Usage Endpoint](https://api.x.com/2/usage/tweets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, or Markdown research notes with tweet links, engagement metadata, cost estimates, and optional saved draft files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can cache query results locally, save Markdown drafts, and maintain a local watchlist for account monitoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
