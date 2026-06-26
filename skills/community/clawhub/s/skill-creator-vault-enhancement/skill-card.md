## Description: <br>
Create or update AgentSkills. Use when designing, structuring, or packaging skills with scripts, references, and assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design, structure, validate, package, and update AgentSkills, including skills that declare vault-backed credential requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update persistent skill files that may influence future agent behavior. <br>
Mitigation: Confirm the intended output location and review generated or modified skill files before placing them in an auto-loaded skills directory. <br>
Risk: Generated scripts or credential instructions could mishandle secrets if reviewed carelessly. <br>
Mitigation: Review generated scripts and credential sections, and use vault-backed environment variables instead of plaintext keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/skill-creator-vault-enhancement) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update skill files and packaging artifacts when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
