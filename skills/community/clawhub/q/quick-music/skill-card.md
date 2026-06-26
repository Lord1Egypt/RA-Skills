## Description: <br>
轻量快捷的音乐搜索工具。一条命令搜歌、拿播放链接，零依赖即开即用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangalexhy](https://clawhub.ai/user/zhangalexhy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search for songs or artists from the command line, page through results, and fetch a playback link for a selected result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Song and artist searches are sent to third-party music API providers. <br>
Mitigation: Avoid sensitive queries and install only when third-party API use is acceptable. <br>
Risk: Returned playback, detail, cover, or lyric links come from external services. <br>
Mitigation: Treat returned links as external content and review them before relying on or sharing them. <br>


## Reference(s): <br>
- [Quick Music on ClawHub](https://clawhub.ai/zhangalexhy/quick-music) <br>
- [Search API endpoint](https://kw-api.cenguigui.cn/) <br>
- [Playback API endpoint](https://api.xcvts.cn/api/music/migu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text CLI output with song lists, playback URLs, and JSON fallback for unresolved responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a required search keyword plus optional page, limit, and play-index arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
