## Description:

Guides analysts, algorithm vendors, and small teams through packaging analytics scripts as trial releases or customer-node-bound production licenses with MGC Blackbox, including a runnable forecasting example.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT

## Use Case:

Developers, independent analysts, and algorithm vendors use this skill to package forecasting, scoring, or data-cleaning scripts for local trials and per-customer deployments. It covers preparation, sealing, delivery, customer import and execution, and renewals, with a sample forecasting workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has no declared tool scope despite detected environment and file-write capabilities.

Mitigation: Review whether environment access and file writing fit the task, and limit execution to the required files and permissions.

Risk: After a package is unsealed, its scripts run with the customer's permissions and can access data and resources available in that environment.

Mitigation: Review the package and run it with only the local access it needs; verify input and output locations and observe network activity during execution.

## Reference(s):

- [MGC-Blackbox project repository](https://github.com/zkeviny/MGC-Blackbox)
- [MGC-Blackbox issue tracker](https://github.com/zkeviny/MGC-Blackbox/issues)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Python code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python examples, shell commands, and delivery checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a sample forecast workflow and reusable delivery and licensing templates.]

## Skill Version(s):

1.0.0 (source: skill frontmatter; confirmed by server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
