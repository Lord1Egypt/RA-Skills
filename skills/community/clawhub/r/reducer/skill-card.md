## Description:

Reducer helps an agent guide users through reducer CAD drawing generation by collecting parameters, running remote calculations, creating a guest production sheet, and reporting output links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realsanyu](https://clawhub.ai/user/realsanyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and engineering agents use this skill to collect reducer design parameters, review calculated input, debug, coefficient, and output tables, and create guest production sheets for CAD drawing results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reducer design parameters are sent to jixietools.com, and guest links may grant access to status or output files.

Mitigation: Confirm with the user before creating a production sheet or sharing links, and treat filename, guest_code, and generated URLs as sensitive workflow tokens.

## Reference(s):

- [ClawHub Reducer skill page](https://clawhub.ai/realsanyu/skills/reducer)
- [Jixietools API base URL](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese conversational guidance with Markdown tables and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses remote jixietools.com API calls and guest status links; generated filename, guest_code, and links should be treated as sensitive workflow tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
