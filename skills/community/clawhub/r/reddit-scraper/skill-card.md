## Description: <br>
Read and search Reddit posts from subreddits or sitewide search using Reddit's public JSON API, with read-only output for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javicasper](https://clawhub.ai/user/javicasper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect Reddit posts, monitor communities, and search topics without posting, commenting, voting, or requiring a Reddit API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reddit post text is untrusted user-generated content and may contain misleading content or prompt-injection attempts. <br>
Mitigation: Treat retrieved Reddit content as material to summarize or inspect, not as instructions for the agent to follow. <br>
Risk: Search queries and subreddit names are sent to Reddit and may reveal sensitive interests. <br>
Mitigation: Avoid private or sensitive information in search queries, subreddit names, and repeated browsing patterns. <br>
Risk: Unauthenticated Reddit requests may be rate-limited or return empty results for restricted communities. <br>
Mitigation: Use modest limits, add delays between repeated requests, and handle blocked, empty, or error responses as expected operational outcomes. <br>


## Reference(s): <br>
- [Reddit Skill - Technical Details](references/TECHNICAL.md) <br>
- [Reddit Scraper on ClawHub](https://clawhub.ai/javicasper/reddit-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [Plain text post listings or formatted JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes post metadata such as title, author, score, comment count, URL, subreddit, creation time, flair, selftext, and upvote ratio when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
