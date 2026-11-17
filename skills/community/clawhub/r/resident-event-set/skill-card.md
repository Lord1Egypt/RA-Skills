## Description:

Resident Event Pack helps an agent turn user-supplied resident event names and approved points into a consistent four-to-eight still image pack, one still per named activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan and generate matching resident event still-image packs from confirmed event names, point text, language, destination, and optional brand references. It is aimed at community activity poster and still-set workflows where the agent must avoid inventing missing facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package requests broad Beatra account permissions, including non-image media generation and wallet-spend authority.

Mitigation: Install only when those account powers are acceptable and review the authorization scopes before delegating generation spend.

Risk: The bundled client can silently replace its own package code through automatic updates.

Mitigation: Disable automatic updates before normal use when reviewed code must remain fixed.

Risk: Uninstall and disconnect can affect the shared Beatra device credential when no other Beatra skills remain.

Mitigation: Use the bundled uninstall flow and confirm whether other Beatra skills still rely on the shared connection before removing local state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beatra-ai/skills/resident-event-set)
- [Beatra Package Homepage](https://beatra.ai/skills/resident-event-set)
- [Resident Event Pack Workflow](artifact/references/workflow.md)
- [Installation and Authentication](artifact/references/installation-and-auth.md)
- [Installation Registration](artifact/references/installation-registration.md)
- [MCP Connection](artifact/references/mcp-connection.md)
- [Tasks and Results](artifact/references/tasks-and-results.md)
- [Billing, Errors, and Recovery](artifact/references/billing-errors-and-recovery.md)
- [Automatic Updates and Safety](artifact/references/automatic-updates-and-safety.md)
- [Uninstall and Disconnect](artifact/references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON payload examples, shell commands, and generated image artifact references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans one still per named activity, submits one billable generation per still, and reports task IDs, resolved models, observed dimensions and formats, and net charged credits.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
