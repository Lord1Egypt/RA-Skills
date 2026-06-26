## Description: <br>
Generates AI-assisted weekly report Markdown from local Git history, work notes, and screenshots, then can send the report to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prayone](https://clawhub.ai/user/prayone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and individual contributors use this skill to turn local Git activity and optional screenshots into structured weekly status reports and Feishu updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadly scan local Git history under PROJECT_ROOT and summarize work activity. <br>
Mitigation: Set PROJECT_ROOT to a narrow intended folder and review the generated Markdown before sharing it. <br>
Risk: The Feishu sender can transmit report content automatically and requires Feishu app credentials. <br>
Mitigation: Move Feishu secrets out of the script, verify the recipient, and use scheduled sending only when unattended recurring reports are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/prayone/weekly-report-generator-feishu) <br>
- [周报生成器功能介绍](周报生成器功能介绍.md) <br>
- [安装和配置指南](安装和配置指南.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown report content with shell command and Feishu delivery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Feishu sender reads a report file and sends text content to a configured Feishu recipient.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
