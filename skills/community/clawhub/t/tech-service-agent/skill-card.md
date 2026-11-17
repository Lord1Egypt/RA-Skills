## Description:

Tech Service Agent collects, maintains, updates, reports on, and queries public information about technology-service institutions, including incubators, makerspaces, pilot bases, concept validation centers, technology parks, and specialized enterprises.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to collect official public information about Chinese technology-service institutions, monitor updates, generate daily briefings and DCAR weekly reports, and query institutions by region, type, industry direction, or OPC tag.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Broad Chinese trigger terms may activate the skill when the user did not intend technology-service institution collection or reporting.

Mitigation: Review trigger terms during installation and prefer explicit user direction before starting collection or update workflows.

Risk: Maintaining a SQLite state database for incremental updates can preserve stale, duplicate, or incorrectly scoped public data.

Mitigation: Use user-directed collection, source attribution, update timestamps, and periodic baseline refreshes when maintaining state.

Risk: Generated reports about institutions or policies may be mistaken for subjective evaluations or investment advice.

Mitigation: Keep outputs limited to official public information, label sources and update times, and avoid subjective institutional ratings or investment recommendations.

## Reference(s):

- [Tech Service Agent on ClawHub](https://clawhub.ai/golngod/skills/tech-service-agent)
- [golngod publisher profile](https://clawhub.ai/user/golngod)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Markdown tables, source-attributed summaries, briefings, and DCAR reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include information sources, update times, policy deadlines when applicable, and special OPC markings.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
