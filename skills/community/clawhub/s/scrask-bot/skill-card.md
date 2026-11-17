## Description:

When a user sends a screenshot through a connected chat surface, Scrask parses it for events and tasks with a configured vision LLM, emits structured intent, and lets the agent delegate calendar or task creation to installed destination skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devsandip](https://clawhub.ai/user/devsandip)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use Scrask to turn screenshots from chat, email, social posts, or invitations into calendar events, reminders, or tasks. The skill is useful when users want the agent to extract actionable items and route them to their installed calendar or task tools with targeted clarification when confidence is low.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots may be processed by configured external vision providers.

Mitigation: Install only when users are comfortable sending screenshot content to the configured provider, and redact sensitive screenshots before use.

Risk: Clearly extracted items may be added to calendar or task tools without a final preview approval.

Mitigation: Enable a confirmation-before-write policy or require user confirmation for automatic destination-skill dispatch.

Risk: Broad invocation aliases may cause the skill to run on screenshots the user did not intend to process.

Mitigation: Narrow trigger aliases or prefer explicit invocation in deployments with sensitive chat surfaces.

Risk: Unpinned dependencies can change parser behavior or supply-chain exposure over time.

Mitigation: Pin and review Python dependencies before deployment.

## Reference(s):

- [Scrask ClawHub listing](https://clawhub.ai/devsandip/skills/scrask-bot)
- [Architecture overview](docs/ARCHITECTURE_OVERVIEW.md)
- [Decision flow](docs/decision-flow.md)
- [Example walkthrough](docs/example-walkthrough.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chat-facing text plus structured JSON intent and shell-command examples in documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parser output includes confidence scores, clarification prompts, destination routing hints, and summary text for the agent to relay.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter declares 4.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
