## Description: <br>
Security-first skill vetting for AI agents before installing skills from ClawHub, GitHub, or other sources, checking red flags, permission scope, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aysun168](https://clawhub.ai/user/aysun168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and agents use this skill to review third-party skills before installation and document red flags, required permissions, risk level, and installation verdicts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publisher and package identity may be confused because the artifact metadata slug differs from the release slug. <br>
Mitigation: Confirm the ClawHub publisher aysun168, release page, and package slug before installing or relying on the skill. <br>
Risk: The skill includes optional GitHub curl examples that contact external URLs when adapted and run. <br>
Mitigation: Review and replace placeholders with trusted repositories only, and inspect responses before using fetched content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aysun168/skill-vetter-bak) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a structured skill vetting report with risk level, verdict, permissions, and red flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
