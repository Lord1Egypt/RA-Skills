## Description: <br>
Search, install, and create OpenClaw skills using intelligent matching across built-in, local, and GitHub skill repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris6970barbarian-hue](https://clawhub.ai/user/chris6970barbarian-hue) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to search known, local, and GitHub-hosted OpenClaw skills, install selected GitHub skills, list installed skills, and create new skill templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install third-party GitHub skills and write local executable skill files with weak scoping and validation. <br>
Mitigation: Install only when you intentionally want a tool that can add or create OpenClaw skills, inspect GitHub repositories and owners before installation, and avoid running the skill with elevated privileges. <br>
Risk: The skill records install history in a local config file. <br>
Mitigation: Review or clear the config and history file when local installation records should not be retained. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chris6970barbarian-hue/skillstore) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Terminal text with generated Markdown, JavaScript, JSON, and git shell command effects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local skill files, config history, and cloned GitHub skill repositories when users choose install or create actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
