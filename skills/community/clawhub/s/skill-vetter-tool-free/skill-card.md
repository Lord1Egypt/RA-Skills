## Description: <br>
Skill安全审查(免费版) helps agents perform a local pre-installation security review of third-party skills using source checks, red-flag detection, permission review, and risk classification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill before installing a third-party skill to review source trust, scan for common red flags, assess requested permissions, and produce a risk classification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may cause the skill to be used for general data analysis instead of skill security vetting. <br>
Mitigation: Use it only for security review tasks and confirm the target is a specific skill directory. <br>
Risk: Review commands can scan sensitive local folders if aimed at a home, credential, or configuration directory. <br>
Mitigation: Limit scans to the skill directory being reviewed and avoid home, credential, and configuration paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/skill-vetter-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with checklists, command examples, and structured report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for local, manual security review of a specific skill directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
