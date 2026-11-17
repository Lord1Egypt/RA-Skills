## Description:

Keep a live app healthy with error alerts, scheduled health checks, code review, cautious auto-merge, project reviews, backups, and recovery guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipposk](https://clawhub.ai/user/philipposk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Shipyard can maintain a live app with error logging, scheduled checks, pull request review, guarded automation, data backups, and incident response guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A request about logs may expand into a broader app upgrade without a clear choice to approve that scope.

Mitigation: Keep work limited to the selected app and task; require a separate plan and approval before broader upgrades.

Risk: Backups can contain users' personal data.

Mitigation: Keep backups protected and private; do not copy them into shared cloud folders or send them through chat.

## Reference(s):

- [ClawHub release: Shipyard ops](https://clawhub.ai/philipposk/skills/shipyard-ops)
- [Error alerts and logs](artifact/references/errors.md)
- [Scheduled health checks](artifact/references/health.md)
- [Code review on pull requests](artifact/references/review.md)
- [Auto-merge rules](artifact/references/automerge.md)
- [Project review](artifact/references/project-review.md)
- [Backups](artifact/references/backups.md)
- [Self-healing workflow](artifact/references/self-healing.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands and code or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the full Shipyard plugin; for non-Shipyard apps, it directs users to the separate upgrade guide.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
