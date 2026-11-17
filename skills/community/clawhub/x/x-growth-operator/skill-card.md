## Description:

Plan and execute mission-driven X growth operations / 任务驱动的 X 增长运营规划与执行。Use when the user wants to monitor KOL posts, detect emerging discussions, turn briefs or uploaded docs into a growth mission, draft replies or posts, rank opportunities, and execute approved actions with a local audit trail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmywangjimmy](https://clawhub.ai/user/jimmywangjimmy)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, founders, and growth teams use this skill to turn a brief into a review-first X growth mission, monitor opportunities, rank them, draft posts or interactions, and execute approved X actions with an audit trail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post publicly from the user's X account when live credentials are configured.

Mitigation: Run in review or dry-run mode by default, require explicit approval before live execution, and configure live OAuth credentials only for accounts authorized to publish.

Risk: The local dashboard can trigger live X posts without a server-side approval check.

Mitigation: Do not run the dashboard with live credentials until server-side approval, authentication, and CSRF protection are added.

Risk: Imported X data may render unsafely in the dashboard.

Mitigation: Avoid loading untrusted imported content in the dashboard until safe DOM rendering is implemented.

Risk: X credentials and local state are stored in local files.

Mitigation: Keep scripts/.env private, avoid publishing generated data paths, and restrict X_API_BASE_URL to official HTTPS X origins.

Risk: Desearch live import may send search queries to an external service.

Mitigation: Disclose Desearch egress before use and only set DESEARCH_API_KEY when live search is needed.

Risk: Node dependencies are declared without a lockfile in the artifact evidence.

Mitigation: Use pinned npm dependencies with a lockfile before deploying the skill in a controlled environment.

## Reference(s):

- [Mission Schema](references/mission-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/jimmywangjimmy/skills/x-growth-operator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces mission, opportunity, action-plan, action, execution-log, memory, and feedback files under local data paths when run.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
