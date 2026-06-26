## Description: <br>
Search, retrieve, and install Agent Skills from the prompts.chat registry using MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengxinjipai](https://clawhub.ai/user/zhengxinjipai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to discover reusable Agent Skills, inspect skill metadata and files, and install selected skills into Claude for later activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add third-party skill files into a persistent Claude skills folder with limited safeguards. <br>
Mitigation: Review the fetched skill author, SKILL.md, filenames, scripts, and configuration files before installation, and avoid installing skills that request broad access or contain unexpected helper code. <br>
Risk: Installed third-party skills may later influence agent behavior when they activate. <br>
Mitigation: Install only skills from publishers and sources the user trusts, and scan or inspect installed files before relying on them in normal workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhengxinjipai/skill-lookup-tool) <br>
- [Publisher profile](https://clawhub.ai/user/zhengxinjipai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with tool-call examples and installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in persistent skill files being written under a Claude skills directory when the user chooses to install a retrieved skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
