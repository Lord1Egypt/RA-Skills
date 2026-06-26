## Description: <br>
Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h-harry](https://clawhub.ai/user/h-harry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and agent users use this skill to vet third-party skills before installation by checking source trust, code behavior, permission scope, and risk level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security verdict is suspicious because related ClawHub and Convex helper workflow skills may launch nested review automation with broad filesystem authority and sandbox bypass. <br>
Mitigation: Install only after manual review, prefer helper execution without yolo or full-access review modes, and require explicit confirmation before actions that affect live services or publish public proof. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with checklists, a vetting report template, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a human-readable skill vetting report; does not execute scanner logic itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
