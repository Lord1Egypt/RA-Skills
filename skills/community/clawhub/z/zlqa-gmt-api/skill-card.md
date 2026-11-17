## Description:

Supports automated testing for ZLQA game GM tool APIs, including test case management, execution, and HTML report viewing after binding a local project path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gerburmsidep7](https://clawhub.ai/user/gerburmsidep7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to initialize a trusted ZLQA checkout, discover GM API test interfaces, run selected or grouped test cases, and inspect generated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit and execute project-local Python test scripts from a mutable external checkout.

Mitigation: Use only with a trusted ZLQA checkout and review the project test scripts before running them.

Risk: Test configuration may contain server addresses, signing keys, accounts, roles, or other sensitive data.

Mitigation: Avoid real production secrets in markdown configuration files and keep the checkout out of shared commits unless secrets are excluded.

Risk: Generated HTML reports are opened automatically after test execution.

Mitigation: Review generated reports as local artifacts from trusted test code before sharing or opening them in broader environments.

## Reference(s):

- [ZLQA-GMT-API-Test ClawHub listing](https://clawhub.ai/gerburmsidep7/skills/zlqa-gmt-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and console-style text with generated HTML test reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit project-local test runner configuration, execute Python test scripts, and open generated HTML reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
