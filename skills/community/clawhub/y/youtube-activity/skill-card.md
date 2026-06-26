## Description: <br>
Manage activities on YouTube by guiding an agent to list channel activity through the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to set up yutu credentials and list YouTube activity such as uploads, likes, and favorites from a channel or authenticated account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on sensitive YouTube OAuth files such as client_secret.json and youtube.token.json. <br>
Mitigation: Keep credential and token files private, store them outside shared or source-controlled folders, add them to .gitignore when working in repositories, and revoke or rotate exposed tokens. <br>
Risk: The skill relies on the third-party yutu CLI to access YouTube APIs. <br>
Mitigation: Install yutu only from trusted sources and review the CLI source or package before using it with YouTube credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/OpenWaygate/youtube-activity) <br>
- [Yutu Project Homepage](https://github.com/eat-pray-ai/yutu) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [Activity List Reference](references/activity-list.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance targets yutu activity commands; yutu command output may be table, JSON, or YAML depending on flags.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
