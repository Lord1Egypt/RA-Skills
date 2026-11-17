## Description:

Turn seller-supplied new-year store mood notes into one retail playlist of 8 to 15 instrumentals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External retail sellers and store operators use this skill to turn already-written new-year store mood notes into a reusable instrumental playlist for doors-open, browsing, checkout, and closing periods. The agent plans the track list, confirms live Beatra credit cost before paid generation, and helps deliver generated results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend Beatra credits when generating music.

Mitigation: Review the live model price and frozen generation card before approval, and do not submit paid calls until the user explicitly approves the work and cost.

Risk: The skill stores and reuses a shared Beatra device token with broad account permissions.

Mitigation: Install only if the Beatra account-wide permission model is acceptable, keep the token only in the private credential file, and never expose it in chat, logs, command arguments, or environment variables.

Risk: Silent automatic package updates are enabled by default.

Mitigation: Disable automatic updates with `python3 scripts/mcp_client.py update --auto off` when a reviewed, stable package is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/retail-new-year-pack)
- [Beatra skill homepage](https://beatra.ai/skills/retail-new-year-pack)
- [New-year retail playlist workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [MCP connection](references/mcp-connection.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated music task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce generated audio artifacts through Beatra after explicit cost confirmation.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
