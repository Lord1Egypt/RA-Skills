## Description:

Travel maintains a local travel system of record for wishlists, documents, entry checks, reservations, budgets, disruptions, loyalty, and trip debriefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to keep durable travel records and get advice on entry readiness, booking deadlines, trip costs, disruptions, companions, long stays, loyalty, and post-trip debriefs. It prepares decisions and records outcomes, but does not execute purchases, bookings, cancellations, or claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to maintain a long-term local archive containing travel, booking, health, finance, contact, vehicle, and travel-history records.

Mitigation: Install it only when that persistence is desired, keep the configured local paths access-controlled, and review file changes regularly.

Risk: The security evidence notes automatic reads and updates of sensitive shared files without clear per-change user approval.

Mitigation: Use agent settings or review practices that surface file changes before retaining them, and rely on the skill's write-disclosure behavior to audit what changed.

Risk: Travel records may include booking locators, document details, health constraints, and finance context.

Mitigation: Redact booking locators where practical and store credentials or full document numbers only as external pointers or last-four summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/travel)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Clawic Travel skill page](https://clawic.com/skills/travel)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain-text guidance with local record updates when durable travel information is produced]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may read and update local Clawic travel, booking, contact, health, pet, vehicle, finance, and profile files.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
