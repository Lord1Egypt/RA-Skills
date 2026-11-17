## Description:

Super Dev Skill transforms PRD documents into SwiftUI iOS application projects with MVVM structure, generated models, views, services, build instructions, and QA handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn product requirements documents into generated SwiftUI iOS projects, including MVVM code structure, persistence and networking components, validation expectations, and follow-up QA review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PRDs may contain confidential product plans or user data that would be included in generated code or shared with the QA handoff workflow.

Mitigation: Review and redact sensitive PRD content before use, and only run the skill when the dev-output generation and qa-skill review flow is acceptable.

Risk: Generated SwiftUI projects may require manual correction before they compile or meet product, accessibility, privacy, and App Store expectations.

Mitigation: Build and test the generated Xcode project locally, review the generated code, and treat qa-skill output as review input rather than final approval.

Risk: The skill creates project files under dev-output, which can affect existing generated work in that location.

Mitigation: Run the skill in a clean workspace or inspect dev-output before generation so important local files are preserved.

## Reference(s):

- [Super Dev Skill on ClawHub](https://clawhub.ai/subaru0573/skills/super-dev-skill)
- [Publisher profile: subaru0573](https://clawhub.ai/user/subaru0573)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated Swift, SwiftUI project files, Xcode build instructions, and QA handoff notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated projects are described as being created under dev-output and passed to qa-skill for review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
