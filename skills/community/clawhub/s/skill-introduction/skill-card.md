## Description: <br>
Generate a beautiful, deployable HTML introduction page for any AgentSkill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent maintainers use this skill to turn a skill directory into a polished HTML introduction page from USAGE.md or SKILL.md. It can generate a local page and optionally publish through a user-configured deploy hook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured deploy hook can execute a user-provided command with normal user permissions. <br>
Mitigation: Run with --no-deploy unless deployment is intended, and set SKILL_INTRO_DEPLOY_CMD only to a deploy script you control. <br>
Risk: Generated documentation can be incomplete or overly technical when the source skill lacks human-facing documentation. <br>
Mitigation: Prefer USAGE.md for public pages and review generated HTML before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songhonglei/skill-introduction) <br>
- [Mistune documentation](https://mistune.lepture.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [HTML file with Markdown guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a local HTML page by default; optional deployment is controlled by a user-configured deploy hook.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
