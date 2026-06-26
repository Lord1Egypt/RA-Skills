## Description: <br>
Build-in-public companion for indie hackers — content workflow, Twitter engagement, project soul creation. A living assistant, not a tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Humanji7](https://clawhub.ai/user/Humanji7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators and indie hackers use SoloBuddy to manage build-in-public ideas, draft social posts, review Twitter content strategy, monitor optional engagement opportunities, and create project personality profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide publishing actions such as committing and pushing draft content. <br>
Mitigation: Inspect generated drafts and proposed git changes before publishing or pushing content. <br>
Risk: Optional Twitter monitoring may run background automation and handle X/Twitter session tokens. <br>
Mitigation: Enable the monitor only after reviewing the scripts, understanding how to stop them, and avoiding storage of session tokens in shell startup files when possible. <br>
Risk: The configured data path may expose unrelated local files if it points at a broad or sensitive directory. <br>
Mitigation: Use a dedicated solobuddy.dataPath folder that contains only SoloBuddy ideas, drafts, and data. <br>


## Reference(s): <br>
- [SoloBuddy ClawHub Page](https://clawhub.ai/Humanji7/solobuddy) <br>
- [Soul Wizard Reference](references/soul-wizard.md) <br>
- [GitHub Homepage](https://github.com/gHashTag/bip-buddy) <br>
- [ClawdBot](https://clawd.bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose draft content, Telegram button payloads, project personality JSON, and command sequences that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
