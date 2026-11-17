## Description:

Automates browser tasks across coordinated roles to map sites, plan workflows, execute approval-aware browser actions, and verify results on sites without usable APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t3ratech](https://clawhub.ai/user/t3ratech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to delegate web workflows to a coordinated browser, research, and review team when a site does not expose a usable API. It is intended for supervised navigation, evidence capture, workflow execution, and result verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can perform sensitive site workflows such as purchases, account changes, posting, financial actions, or account updates.

Mitigation: Keep approvals enabled for sensitive actions and review proposed browser steps before execution.

Risk: The skill can use browser, file, memory, agent, and MCP tools when available, which may expose data or broaden workflow effects.

Mitigation: Grant only the tools needed for the task, scope memory and MCP access deliberately, and review captured evidence before reuse.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/t3ratech/skills/web-automation-team)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with role plans, browser action steps, evidence summaries, review feedback, and optional command or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing coordination, research, browser workflow, and review outputs; no bundled executable code.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
