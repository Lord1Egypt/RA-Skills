## Description:

Integrates Datto Autotask with Membrane so agents can discover and run actions for tickets, contacts, projects, automations, reports, and related PSA records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and MSP or IT service teams use this skill to connect an agent to Datto Autotask through Membrane, discover available actions, and run or create actions that update PSA records and generate reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create actions and change Datto Autotask tickets, contacts, projects, automations, and other business records.

Mitigation: Use least-privilege Autotask credentials and require explicit user confirmation before record-changing actions.

Risk: The skill relies on an unpinned third-party Membrane CLI installation.

Mitigation: Pin the Membrane CLI to a reviewed version before use and review updates before upgrading.

Risk: The integration requires an agent-mediated connection to a business application.

Mitigation: Install only in environments where users trust Membrane and can review the requested connection scope.

## Reference(s):

- [Membrane homepage](https://getmembrane.com)
- [Datto Autotask official documentation](https://ww1.autotask.net/help/Content/home.htm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-oriented CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, a Membrane account, and an authenticated Datto Autotask connection.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
