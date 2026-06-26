## Description: <br>
面向全国科技行业厂家和集成商的标讯情报工具，每日采集多源招标信息，按省份和关键词生成商机摘要、日报、周报和推送内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongliw2006](https://clawhub.ai/user/yongliw2006) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sales teams, system integrators, IT service providers, and managers use this skill to find timely tender opportunities across China's technology, security, networking, and information systems markets. It supports manual searches, report generation, data-quality checks, keyword management, and workspace push notifications. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: One report mode runs an unbundled workspace script through a shell. <br>
Mitigation: Review and trust the workspace scripts before using report mode, especially any scripts/generate-report-v8.mjs file. <br>
Risk: The skill requests tender-site cookies and a Feishu webhook secret. <br>
Mitigation: Provide those secrets only in a trusted workspace and only after confirming which local scripts read and use them. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/yongliw2006/tender-intelligence) <br>
- [Data Sources Reference](references/data-sources.md) <br>
- [Gansu Cities Reference](references/gansu-cities.md) <br>
- [User Guide](USER_GUIDE.md) <br>
- [Report Sections Specification](docs/SECTIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown reports with inline Node.js commands and configuration requirements] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and tender-site cookies plus a Feishu webhook for configured collection and push workflows.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
