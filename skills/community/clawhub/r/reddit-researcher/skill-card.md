## Description: <br>
Search and analyze Reddit posts and comments to summarize user opinions, troubleshoot issues, and track trends across communities and topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zachgodsell93](https://clawhub.ai/user/zachgodsell93) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, researchers, and product teams use this skill to gather Reddit discussions, inspect posts and comments, and summarize community sentiment for product research, troubleshooting, market analysis, competitive intelligence, and content research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries, subreddit names, and public-user lookups are sent to Reddit. <br>
Mitigation: Install only when that disclosure is acceptable, and prefer anonymous access when its rate limits are sufficient. <br>
Risk: Optional Reddit OAuth credentials can be exposed through logs, shared terminals, or version control. <br>
Mitigation: Use a dedicated Reddit app and account, keep the client secret out of logs and repositories, and rotate credentials periodically. <br>
Risk: Reddit rate limits can interrupt research workflows. <br>
Mitigation: Use OAuth for higher limits when appropriate, add delays between requests, respect 429 responses, and cache results when practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zachgodsell93/reddit-researcher) <br>
- [Reddit app preferences](https://www.reddit.com/prefs/apps) <br>
- [Reddit OAuth access token endpoint](https://www.reddit.com/api/v1/access_token) <br>
- [Reddit JSON API base](https://www.reddit.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Reddit API request examples, jq filters, summaries, findings, notable discussions, recommendations, and data-point counts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
