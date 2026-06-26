## Description: <br>
Fetches recent articles from WeChat public accounts through the wcrss.com API and helps an agent summarize and display them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blackomw](https://clawhub.ai/user/blackomw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve recent WeChat public account articles from a configured wcrss.com account, inspect individual article records, and produce concise article summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a WCRSS_API_KEY from the local environment to contact api.wcrss.com. <br>
Mitigation: Use a dedicated wcrss.com API key, keep it in environment variables, and rotate or revoke it if the workspace is shared or exposed. <br>
Risk: Fetched article and publisher data are cached locally in wechat_articles_cache.json. <br>
Mitigation: Clear the cache when article content should not remain on disk, especially on shared machines or temporary workspaces. <br>
Risk: Article HTML is passed to the assistant for summarization. <br>
Mitigation: Review whether fetched article content is appropriate to process before asking the assistant to summarize it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/blackomw/wechat-rss) <br>
- [WCRSS](https://wcrss.com/) <br>
- [WCRSS publishers](https://wcrss.com/publishers) <br>
- [WCRSS settings](https://wcrss.com/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON article records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WCRSS_API_KEY; fetch accepts recentDays and num arguments; article and publisher data are cached locally for one hour.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
