## Description:

Operate Skool communities with onboarding, classroom planning, calendar cadence, official automations, and safer member lifecycle workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External community operators and creators use this skill to plan and run Skool groups, onboarding, classroom access, calendars, official automations, and member lifecycle decisions while keeping member-impacting actions explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Skool operating notes could accumulate more member detail than needed.

Mitigation: Store only durable group-level operating rules, approved workflows, and incident lessons in ~/skool/ after user consent; avoid raw DMs, payment details, and full member histories.

Risk: Invites, removals, course access changes, DM automation, and billing-adjacent edits can affect real members.

Mitigation: Keep the skill in preview or advisory mode until the user explicitly approves the action, payload, affected group, and rollback path.

Risk: Unsupported Skool automation can create fragile or misleading operational guidance.

Mitigation: Prefer native Skool settings, AutoDM, Zapier, documented webhooks, and official help documentation; make unsupported automation limits explicit before proposing custom workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/skool)
- [Clawic skill homepage](https://clawic.com/skills/skool)
- [Official Skool help center](https://help.skool.com)
- [SKILL.md](artifact/SKILL.md)
- [Official Surface - Skool](artifact/official-surface.md)
- [Automation and Integrations - Skool](artifact/automation-and-integrations.md)
- [Member Lifecycle - Skool](artifact/member-lifecycle.md)
- [Troubleshooting - Skool](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with optional local setup commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain durable operating notes in ~/skool/ after user consent; live member, invite, access, DM, automation, or billing-adjacent changes require explicit confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
