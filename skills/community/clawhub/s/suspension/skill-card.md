## Description:

Guides users through a Chinese-language suspension CAD drawing workflow for selecting a suspension product, collecting design parameters, calculating results, and creating a guest production sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External users and mechanical design practitioners use this skill to collect suspension design inputs one at a time, call the JixieTools suspension workflow, review calculated parameters, and generate a no-login production sheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suspension design inputs are sent to jixietools.com, and the resulting production sheet is exposed through a no-login guest link.

Mitigation: Use the workflow only when sending the design data to that external service and receiving a guest production link is acceptable; avoid proprietary or confidential engineering data unless that workflow is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liv09370/skills/suspension)
- [JixieTools API base](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-language Markdown with tables and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces stepwise prompts, calculated result summaries, production-sheet links, and progress updates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
