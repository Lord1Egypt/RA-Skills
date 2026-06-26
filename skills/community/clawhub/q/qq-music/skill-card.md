## Description: <br>
Provides summary data for public QQ Music playlists, songs, and artists, including play counts, favorites, and ranking trends without download or bulk scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike47512](https://clawhub.ai/user/mike47512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to summarize and compare public QQ Music playlists, songs, artists, and ranking pages for lightweight trend monitoring. It is scoped to visible public page information and avoids downloads, interface reverse engineering, and bulk collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A logged-in browser session may expose personal QQ Music page information to the agent. <br>
Mitigation: Use the skill for public page summaries; avoid private account workflows and review any logged-in page content before sharing or retaining it. <br>
Risk: Over-automation could conflict with QQ Music platform rules or trigger anti-abuse controls. <br>
Mitigation: Keep usage lightweight, avoid downloads, interface reverse engineering, and bulk scraping, and control request frequency. <br>
Risk: Dynamic rendering and human verification pages can make extracted metrics incomplete or stale. <br>
Mitigation: Open pages manually when needed, confirm rendered content before analysis, and treat extracted trend summaries as reviewable signals. <br>


## Reference(s): <br>
- [QQ Music](https://y.qq.com/) <br>
- [QQ Music Toplist](https://y.qq.com/n/ryqq/toplist) <br>
- [QQ Music Search](https://y.qq.com/n/ryqq/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown or concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include visible public QQ Music page links and playlist, song, artist, play-count, favorite-count, ranking, genre, language, and duration fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
