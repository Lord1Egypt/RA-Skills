## Description: <br>
Monitors home pet videos for restricted-area entry, dining-table climbing, and trash rummaging, then returns alerts, structured results, recommendations, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet owners and home-monitoring developers use this skill to analyze pet monitoring images or videos for restricted-zone intrusion, table climbing, and trash rummaging. Agents can also query cloud-hosted historical warning reports and present the results as Markdown tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends pet-monitoring photos or videos to Life Emergence cloud APIs for analysis. <br>
Mitigation: Use it only with household media that is acceptable to upload to that cloud service, and avoid footage containing sensitive people, rooms, documents, or devices. <br>
Risk: The skill silently creates or reuses a local account identity and can persist account tokens in a workspace SQLite database. <br>
Mitigation: Run it in a controlled workspace, avoid shared machines, and inspect or delete the workspace data directory, including smyx-api-key.txt and smyx-common-claw.db, after use when identity persistence is not desired. <br>
Risk: Automated restricted-area alerts can be incomplete or incorrect. <br>
Mitigation: Treat results as home-monitoring assistance and confirm the actual scene before acting on an alert. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-restricted-area-warning-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API reference](artifact/references/api_doc.md) <br>
- [Common analysis API reference](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports or tables, structured JSON, report links, and command-line execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local video files or public URLs; documented video formats are mp4, avi, and mov with a 10 MB maximum.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter lists 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
