## Description: <br>
Security-first skill vetting for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingze00000](https://clawhub.ai/user/bingze00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review ClawHub, GitHub, or other sourced skills before installation. It guides source checks, full-file review, permission scoping, risk classification, and a written vetting report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes optional GitHub curl examples that access public remote URLs. <br>
Mitigation: Treat the commands as optional lookups, verify the repository owner and path before running them, and keep review activity limited to the skill or source being evaluated. <br>
Risk: The skill provides a checklist and cannot replace human judgment for sensitive installations. <br>
Mitigation: Require human approval for skills involving credentials, account actions, system changes, or broad local access. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with checklist items and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a structured skill vetting report with red flags, requested permissions, risk level, verdict, and notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
