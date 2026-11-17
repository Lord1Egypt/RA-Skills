## Description:

Builds a total addressable market from an approved ideal customer profile, estimates sourcing costs, and deploys the resulting company list as a Cargo model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue operations, go-to-market engineering, and sales teams use this skill to define and size an account universe, approve its sourcing cost, and make the sourced companies available to other Cargo workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid company sourcing can exceed the intended budget if a filter is too broad or a limit is unclear.

Mitigation: Count the candidate pool, confirm live connector pricing, and obtain approval for the filter, limit, and maximum spend before sourcing.

Risk: Installing dependencies or deploying adapted resources may introduce unwanted changes.

Mitigation: Confirm trust in the current Cargo CLI and cargo-cdk dependency versions, and review the CDK plan before deployment.

Risk: ICP research and sourcing may use website, customer-story, or LinkedIn company data without appropriate permission.

Mitigation: Confirm authorization to use each data source before researching or sourcing companies.

## Reference(s):

- [Cargo GTM skills repository](https://github.com/getcargohq/gtm-skills)
- [TAM-building skill source](https://github.com/getcargohq/gtm-skills/tree/main/tam-building)
- [ClawHub skill release](https://clawhub.ai/cargo-ai/skills/tam-building)
- [Configuration guide](artifact/references/configure.md)
- [Sourcing alternatives](artifact/references/sources.md)
- [Run and reporting guide](artifact/references/run.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown report with TypeScript configuration and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides deployment of one Cargo company model after operator approval of the filter, limit, and maximum spend.]

## Skill Version(s):

0.5.2 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
