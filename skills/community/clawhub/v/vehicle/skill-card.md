## Description:

Vehicle guides Chinese-language vehicle engineering general design CAD drawing generation through product selection, parameter collection, calculation, incremental edits, production-sheet creation, and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External vehicle-design users and engineers use this skill to collect required vehicle parameters, run JixieTools vehicle design calculations, review calculated outputs, create a guest production sheet, and monitor the resulting CAD drawing workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vehicle design inputs are sent to the external jixietools.com service.

Mitigation: Require explicit user confirmation before each network call and avoid submitting confidential or sensitive design data.

Risk: Generated production sheets are exposed through guest-accessible links.

Mitigation: Treat returned links as shareable access links and disclose or store them only for intended recipients.

Risk: Shell command templates with interpolated JSON can be fragile or unsafe if values are inserted literally.

Mitigation: Build requests with a safe HTTP client or JSON serializer, and review commands before execution.

## Reference(s):

- [Vehicle Skill on ClawHub](https://clawhub.ai/liv09370/skills/vehicle)
- [JixieTools API Base](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown with tables and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides step-by-step confirmation, parameter collection, API calculation review, incremental updates, and production-sheet progress checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
