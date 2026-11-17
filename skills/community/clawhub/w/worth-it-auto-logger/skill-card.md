## Description:

Automatically detects active projects, tracks session time, identifies value and cost signals during conversations, and logs ROI entries to Worth It.

This skill is ready for commercial/non-commercial use.

## Publisher:

[storyscriptapp](https://clawhub.ai/user/storyscriptapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users install this companion skill with Worth It so an agent can detect active work, estimate time saved or money earned, log API costs, and send ROI records without manual commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill silently monitors conversations and sends inferred project, activity, time, cost, and revenue records to the Worth It API.

Mitigation: Install only when automatic ROI tracking is desired, notify affected users, and confirm data storage, review, deletion, pause, and disable controls before use.

Risk: Automatically inferred ROI entries can be incorrect or over-counted.

Mitigation: Review logged records regularly, tune confidence thresholds, and delete or correct inaccurate entries in Worth It.

## Reference(s):

- [Worth It Auto-Logger on ClawHub](https://clawhub.ai/storyscriptapp/skills/worth-it-auto-logger)
- [Worth It - Agent Profitability Tracker on ClawMart](https://www.shopclawmart.com/listings/worth-it-agent-profitability-tracker-961a92fb)

## Skill Output:

**Output Type(s):** [API calls, JSON, text, guidance]

**Output Format:** [JSON API payloads and occasional plain-text ROI updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batches detected value signals until session end and conditionally emits a short ROI update.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
