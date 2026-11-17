## Description: <br>
数据质量检查基础版 helps an AI agent check quantitative strategy datasets for completeness, accuracy, consistency, and timeliness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an AI agent through local checks of price and factor data, including missing data, abnormal values, price-volume consistency, and stale data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags the release as suspicious because network/API use is under-explained and the skill includes broad environment, file, and command authority. <br>
Mitigation: Review before installing, run only in a scoped workspace, and approve file reads or shell commands only for explicitly selected local datasets. <br>
Risk: The skill's guidance includes an environment-variable check and mentions callback URLs or external API credentials. <br>
Mitigation: Avoid broad environment-variable inspection, and do not provide callback URLs or external API credentials unless the data flow is understood and acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/quant-data-quality-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with code blocks and JSON, text, or CSV result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local file access and shell execution through the hosting agent; the free edition is described as single-task use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
