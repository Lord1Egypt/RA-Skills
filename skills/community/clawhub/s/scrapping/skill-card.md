## Description: <br>
Helps an agent retrieve public social media profiles, posts, videos, comments, follower data, engagement statistics, transcripts, ad library records, trending content, hashtags, creator information, and related public platform data through ScrapeCreators API requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[berthelol](https://clawhub.ai/user/berthelol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to choose ScrapeCreators endpoints and issue safe curl and jq requests for public social media research, creator lookup, content retrieval, ad library checks, and lightweight data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends public handles, URLs, search terms, and similar queries to ScrapeCreators using the user's API key. <br>
Mitigation: Use a dedicated API key where possible, keep the key in SCRAPECREATORS_API_KEY, and avoid placing credentials in scripts, saved command history, or chat transcripts. <br>
Risk: Large public social media exports may contain personal or sensitive public data. <br>
Mitigation: Set clear result and pagination limits, avoid saving raw bulk datasets unless needed, and delete or protect JSON and CSV exports. <br>
Risk: Paginated and high-cost endpoints can consume credits quickly. <br>
Mitigation: Use trim=true, fetch only the pages needed, and reserve high-cost endpoints such as TikTok audience demographics for explicit user requests. <br>


## Reference(s): <br>
- [ScrapeCreators](https://scrapecreators.com) <br>
- [ScrapeCreators API Docs](https://docs.scrapecreators.com) <br>
- [TikTok API Endpoints](references/tiktok.md) <br>
- [Instagram API Endpoints](references/instagram.md) <br>
- [YouTube API Endpoints](references/youtube.md) <br>
- [Twitter/X API Endpoints](references/twitter.md) <br>
- [LinkedIn API Endpoints](references/linkedin.md) <br>
- [Facebook API Endpoints](references/facebook.md) <br>
- [Reddit API Endpoints](references/reddit.md) <br>
- [Other Platform Endpoints](references/other-platforms.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown with inline bash, curl, and jq examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API request guidance and optional JSON or CSV extraction patterns; requires SCRAPECREATORS_API_KEY, curl, and jq.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
