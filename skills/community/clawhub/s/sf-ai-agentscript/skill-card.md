## Description:

Salesforce AI Agent Script helps agents author, validate, preview, publish, and activate deterministic Salesforce Agentforce .agent bundles using the Agent Script DSL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsouza-anush](https://clawhub.ai/user/dsouza-anush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build deterministic Salesforce Agentforce agents, validate Agent Script syntax and runtime patterns, and prepare authoring bundles for preview, publish, and activation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Salesforce CLI validation, publish, activation, deactivation, and deletion examples can change the wrong org if run against an unintended target.

Mitigation: Confirm the target org and prefer sandbox validation before running org-changing commands.

Risk: HTTP callout and production deployment examples may affect live Agentforce behavior.

Mitigation: Review callout, activation, deactivation, and deletion examples before applying them to production.

Risk: Installing an unpinned skill release can introduce unreviewed guidance changes.

Mitigation: Prefer a pinned or organization-approved installer for controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dsouza-anush/skills/sf-ai-agentscript)
- [Agent Script documentation](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-script.html)
- [Agentforce DX guide](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx.html)
- [Salesforce CLI agent commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_agent_commands_unified.htm)
- [Agent Script recipes](https://github.com/trailheadapps/agent-script-recipes)
- [Activation checklist](references/activation-checklist.md)
- [Syntax reference](references/syntax-reference.md)
- [Actions reference](references/actions-reference.md)
- [Production gotchas](references/production-gotchas.md)
- [Version history](references/version-history.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code snippets, shell commands, configuration examples, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Salesforce CLI commands that should be reviewed before execution against a target org.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata version 2.9.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
