## Description: <br>
Security-first skill vetting for AI agents before installing skills from ClawHub, GitHub, or other sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent operators, and security reviewers use this skill to evaluate AI agent skills before installation by checking source trust, permissions, red flags, and risk level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a checklist aid and may not catch every unsafe behavior in another skill. <br>
Mitigation: Treat its output as guidance, then independently review and scan the target skill before installation. <br>
Risk: The optional sample commands make network requests to GitHub when a user chooses to run them. <br>
Mitigation: Run commands only against intended repositories and inspect URLs before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blueworldmarketing/skill-vetter-bwm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown checklist and vetting report with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review guidance only; sample commands are run by the user when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
