## Description: <br>
Scrape quarterly anime lineups from https://yuc.wiki/ and output structured results for a specified or latest quarter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yjl9903](https://clawhub.ai/user/yjl9903) <br>

### License/Terms of Use: <br>
GNU Affero General Public License v3.0 <br>


## Use Case: <br>
Developers and content maintainers use this skill to retrieve seasonal anime lineup data from public yuc.wiki quarter pages and present it as structured results plus a concise airing table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public yuc.wiki pages and may write scraped JSON to a user-directed output path. <br>
Mitigation: Run it only when public website access and the selected output destination are acceptable. <br>
Risk: Website layout changes could reduce parsing accuracy or cause incomplete lineup extraction. <br>
Mitigation: Review the generated table and JSON, and use the manual scrape guide or update selectors if count checks or output quality look suspicious. <br>


## Reference(s): <br>
- [Yuc's Anime List on ClawHub](https://clawhub.ai/yjl9903/yuc) <br>
- [yuc.wiki](https://yuc.wiki/) <br>
- [Manual Scrape Guide](reference/manual_scrape.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [JSON plus a concise Markdown seasonal airing table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source quarter information, grouped titles, status or time, and episode notes; may write scraped JSON to a user-directed path.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release metadata; artifact metadata version 2026.03.07) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
