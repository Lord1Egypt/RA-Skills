## Description: <br>
SkillPress analyzes repeatable workflows from conversations or tasks and generates standard SKILL.md templates plus script scaffolds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxr-666](https://clawhub.ai/user/lxr-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to turn repeatable task patterns into reusable skill documentation and starter script structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates files, and the security summary flags file-writing paths as under-scoped. <br>
Mitigation: Review generated paths before running the skill and set OPENCLAW_WORKDIR to an intended workspace directory. <br>
Risk: Untrusted or complex slugs could affect where generated files are written. <br>
Mitigation: Use simple slugs without slashes, dots, or absolute path components. <br>
Risk: The publisher is third-party and the security verdict is suspicious. <br>
Mitigation: Install only when the publisher is trusted and review the generated SKILL.md and script scaffold before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxr-666/skillpress) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown files and Python script scaffolds, with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated skill files under an OPENCLAW_WORKDIR skills directory or the current directory when unset.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
