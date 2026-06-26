## Description: <br>
Chinese podcast analytics toolkit for discovering trending or rising podcasts and episodes, analyzing competitive categories, tracking subscription trends, and producing creator opportunity reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mteng27](https://clawhub.ai/user/mteng27) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External podcast creators, analysts, and listeners use this agent to discover Chinese podcast trends, compare categories and shows, track subscription movement, and prepare opportunity reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Initialized subscription history may include fabricated past subscriber data that can be mistaken for observed trends. <br>
Mitigation: Use live API metrics or build history from future observations before relying on trend analysis for decisions. <br>
Risk: Podcast search terms and enrichment requests are sent to external podcast services. <br>
Mitigation: Avoid confidential research topics or sensitive campaign terms when querying external APIs. <br>


## Reference(s): <br>
- [API Notes](references/api.md) <br>
- [Output Modes](references/output-modes.md) <br>
- [Title Signals](references/title-signals.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mteng27/xyz-podcast-radar-cn) <br>
- [xyzrank Ranking API](https://xyzrank.com/api/episodes) <br>
- [xyzrank Trend API](https://api.xyzrank.top/v1/stats) <br>
- [Xiaoyuzhou Podcast Pages](https://www.xiaoyuzhoufm.com/podcast/{pid}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text or Markdown analysis, with optional JSON API output and local JSON tracking files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query public podcast ranking, trend, and Xiaoyuzhou pages; subscription tracking can write local JSON history files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and PUBLISH.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
