## Description: <br>
Twitter/X data assistant for retrieving tweet details, user profiles, search results, comments, repost information, and trends through the MaxHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media, marketing, media, and communications teams use this skill to collect and analyze Twitter/X public-interest signals such as brand mentions, tweet discussions, trending topics, and account activity. It supports browse, analysis, and comparison workflows backed by read-only MaxHub API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive MaxHub API key. <br>
Mitigation: Configure MAXHUB_API_KEY through the agent or environment secret mechanism, do not paste key values into chat output, and rotate the key if exposed. <br>
Risk: Server security evidence rated the release suspicious because unrelated Douyin/Xiaohongshu fallback instructions make the runtime scope unclear. <br>
Mitigation: Review the skill before installation and keep execution limited to the documented Twitter/X endpoints unless the unrelated fallback material is removed or clearly isolated. <br>
Risk: The skill collects Twitter/X social data through a third-party API. <br>
Mitigation: Use results for permitted analysis only, respect privacy and data-use requirements, and treat third-party API data as reference material rather than authoritative ground truth. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/new-ironman/twitter-aggregate-scraper) <br>
- [MaxHub website](https://www.aconfig.cn) <br>
- [Tweet Data API](references/api-tweet.md) <br>
- [Search & Trending API](references/api-search-trending.md) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with tables, summaries, links, and inline shell commands for API access when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Matches the user's language, humanizes numbers, avoids exposing API key values, and depends on MAXHUB_API_KEY for authenticated MaxHub requests.] <br>

## Skill Version(s): <br>
3.6.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
