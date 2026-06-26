## Description: <br>
Queries Threads posts, profiles, search results, comments, and reposts through MaxHub read-only APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and social media operators use this skill to search Threads content, fetch post and profile details, inspect comments and reposts, and produce bilingual summaries or analyses from MaxHub API results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive MaxHub API key and sends Threads search terms and request data to a third-party service. <br>
Mitigation: Install only if the user trusts MaxHub/aconfig.cn, configure the key through MAXHUB_API_KEY or the ClawHub secret mechanism, and do not print or paste the key in responses. <br>
Risk: The security scan flags unrelated Douyin/Xiaohongshu fallback routing guidance inside a Threads-only skill. <br>
Mitigation: Constrain use to documented Threads endpoints under https://www.aconfig.cn/api/v1/threads and remove or ignore unrelated fallback routes before deployment. <br>
Risk: Third-party API data is for reference only and can be incomplete, stale, or inaccurate. <br>
Mitigation: Treat generated analysis as advisory and verify important findings against source Threads content or approved analytics systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/new-ironman/threads-aggregate-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/new-ironman) <br>
- [MaxHub API service](https://www.aconfig.cn) <br>
- [Post & User API reference](artifact/references/api-post-user.md) <br>
- [Parameter mappings](artifact/references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, bullet summaries, links, and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Matches the user's detected English or Chinese language, humanizes numeric results, and keeps MAXHUB_API_KEY values out of responses.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
