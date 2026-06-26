## Description: <br>
YouTube 全场景数据查询助手，支持 Web/V2 API workflows for video, channel, search, comments, subtitles, Shorts, and related analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, analysts, and developers use this skill to query YouTube channel, video, search, subtitle, Shorts, playlist, and comment data through MaxHub APIs and turn the returned data into browse results, comparisons, or structured analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires MAXHUB_API_KEY and sends YouTube query data to MaxHub/aconfig.cn. <br>
Mitigation: Install only when the publisher and MaxHub service are trusted, scope the API key where possible, and avoid exposing the key in prompts, logs, or rendered output. <br>
Risk: The security summary flags non-YouTube automatic fallback routes in the artifact. <br>
Mitigation: Review the fallback table before use and remove or disable unrelated Douyin fallback behavior if the deployment should remain YouTube-only. <br>
Risk: The security guidance flags media stream or download endpoints with potential copyright or platform-terms implications. <br>
Mitigation: Use stream and download features only for authorized media-access workflows and communicate limits clearly to users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/new-ironman/youtube-aggregate-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/new-ironman) <br>
- [MaxHub API website](https://www.aconfig.cn) <br>
- [Channel API reference](references/api-channel.md) <br>
- [Search API reference](references/api-search.md) <br>
- [Video API reference](references/api-video.md) <br>
- [Parameter mapping reference](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with tables, bullets, inline links, and curl/API examples when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should match the user's language, summarize API data, keep API keys out of responses, and note endpoint failures or empty results honestly.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
