## Description:

Use rook to test, evaluate, red-team or regression-check an AI agent the user owns, or to interpret saved Rook results. Does not apply to ordinary unit tests, browser automation or web UI checks without an AI agent under test.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rahulj-123](https://clawhub.ai/user/rahulj-123)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent owners use Rook to discover an AI agent, generate and run scoped functional or adversarial scenarios, and review evidence-based results. They can also use the skill to interpret saved Rook reports without starting another run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The standard workflow may sync unspecified project data to a cloud service without making the payload clear or asking for approval.

Mitigation: Before installing, confirm where synchronization sends data and what it includes; avoid uploading sensitive project material unless the disclosure has been reviewed and authorized.

Risk: The security scan is partial because a referenced agent.yaml file was not found, so that reference is not covered by the scan evidence.

Mitigation: Locate and review the referenced agent.yaml, then ensure the security review covers it before relying on the scan.

## Reference(s):

- [CI workflow](references/ci.md)
- [Headless output contracts](references/headless-contract.md)
- [MCP servers](references/mcp.md)
- [Profiles](references/profiles.md)
- [Scenarios](references/scenarios.md)
- [Troubleshooting](references/troubleshooting.md)
- [Verdicts and reporting](references/verdicts.md)
- [Rook CLI installation instructions](https://github.com/LambdaTest/rook#install)
- [ClawHub release page](https://clawhub.ai/rahulj-123/skills/rook-cli)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Shell commands, Configuration instructions, JSON]

**Output Format:** [Guidance and summaries, shell command examples, configuration snippets, and structured Rook report data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected agent, profile, scenarios, and available run evidence.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
