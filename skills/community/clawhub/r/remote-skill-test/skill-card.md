## Description:

Remote Skill Test orchestrates end-to-end testing of agent skills on a remote jump host, including installation, remote execution, report retrieval, and comparison with previous runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panlm](https://clawhub.ai/user/panlm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to validate local agent-skill changes on a remote jump host, retrieve generated reports and logs, and compare current output against a previous run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote agent execution can run with safety checks disabled and may access or modify more than intended on the remote account.

Mitigation: Use a disposable or tightly scoped remote account with no production credentials, and remove skipped-permission or auto-confirm behavior where possible.

Risk: Unsafe SSH and installation patterns can expose the run to host-verification, supply-chain, or command-injection risk.

Mitigation: Enable SSH host verification, pin and verify the skills repository, and validate user-supplied command fields before execution.

Risk: Retrieved logs and reports may contain sensitive information from the remote test environment.

Mitigation: Treat copied logs and reports as sensitive artifacts and review them before sharing or committing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/panlm/skills/remote-skill-test)
- [Publisher Profile](https://clawhub.ai/user/panlm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May retrieve reports and logs and write a test-analysis.md file under ./test-results for a run.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
