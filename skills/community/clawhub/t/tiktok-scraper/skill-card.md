## Description: <br>
Access live TikTok creator, video, comment, transcript, trend, hashtag, and song data through the CreatorCrawl API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonbalfe](https://clawhub.ai/user/simonbalfe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to research TikTok creators, videos, trends, hashtags, songs, comments, and transcripts through CreatorCrawl API lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a CreatorCrawl API key and can issue broad or repeated TikTok lookup requests. <br>
Mitigation: Keep CREATORCRAWL_API_KEY in the environment only, avoid sensitive proprietary research targets, and ask the agent to confirm before broad comment, follower, following, transcript, or repeated lookup requests. <br>


## Reference(s): <br>
- [CreatorCrawl](https://creatorcrawl.com) <br>
- [ClawHub skill page](https://clawhub.ai/simonbalfe/tiktok-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREATORCRAWL_API_KEY and curl; API calls may consume CreatorCrawl credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
