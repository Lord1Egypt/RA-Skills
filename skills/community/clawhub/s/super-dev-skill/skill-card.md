## Description: <br>
Transforms PRD documents into SwiftUI iOS application projects with MVVM structure, UI components, data models, services, and build guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert product requirements into starter SwiftUI iOS projects, including models, view models, views, services, tests, and next-step instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated project files may include incorrect or unsuitable implementation choices for the supplied PRD. <br>
Mitigation: Review the generated project under dev-output/ before opening it in Xcode or using it as production code. <br>
Risk: PRDs that request networking, iCloud, notifications, sharing, or other integrations may produce code that touches real services or user data. <br>
Mitigation: Inspect and test those integrations with non-production credentials and sample data before connecting real services. <br>
Risk: The generated code is passed to qa-skill after project generation. <br>
Mitigation: Install only when this follow-on QA handoff is acceptable for the project contents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-dev-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated Swift code, Xcode project files, and build instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated project files under dev-output/ and passes generated code to qa-skill when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
