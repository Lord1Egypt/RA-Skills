## Description: <br>
技能商店客户端，支持查询在线技能、一键下载安装技能包 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pig-gua](https://clawhub.ai/user/pig-gua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query a local skill-shop service, search available skills, inspect skill details, and install selected skill packages into an OpenClaw skills directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install command can overwrite persistent local skills with unverified downloaded packages. <br>
Mitigation: Use `skill-shop install` only with trusted local services and reviewed packages; back up existing skills before installation. <br>
Risk: Installed skills become persistent executable code in the local OpenClaw skills directory. <br>
Mitigation: Review package contents and source before installation, and treat newly installed skills as executable code until integrity and publisher verification are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pig-gua/skill-shop) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/pig-gua) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3, unzip, and the requests Python package; connects to a local skill-shop service and may write installed skill files to the OpenClaw skills directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
