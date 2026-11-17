## Description:

Navigate Uber Eats in a live browser or app handoff to compare merchants, manage carts, and reach checkout safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when an agent needs to work with their real Uber Eats session to browse merchants, compare delivery details, draft carts, verify checkout information, or recover from order issues. It is scoped to Uber Eats-specific browsing, ordering, fallback, and support workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may interact with a real Uber Eats session containing addresses, payment methods, cart state, and live ordering consequences.

Mitigation: Use only an approved browser or app session, re-read visible state before acting, and require explicit current-thread confirmation before changing delivery details, editing a non-empty cart, or placing an order.

Risk: Optional local memory could capture sensitive account, payment, verification, receipt, or support details if used carelessly.

Mitigation: Keep local notes limited to durable preferences, address labels, merchant patterns, and issue history; do not store passwords, full payment details, one-time codes, sensitive receipts, or raw support transcripts.

Risk: Blocked, blank, or access-denied web sessions can make automation unreliable.

Mitigation: Stop blind interaction, verify the page state, and switch to locale routes, app handoff, manual guidance, or support recovery when the browser session is not trustworthy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/uber-eats)
- [Publisher Profile](https://clawhub.ai/user/ivangdavila)
- [Uber Eats](https://www.ubereats.com)
- [Uber Eats Help](https://help.uber.com/ubereats)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use optional local notes in ~/uber-eats/ when the user approves persistent memory.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
