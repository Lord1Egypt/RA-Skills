## Description:

Turn an offer into a concrete multi-step sales funnel spec - page-by-page structure, price ladder, copy outline and the metrics each step must hit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autonnel](https://clawhub.ai/user/autonnel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn an online offer into a build-ready sales funnel plan, including the funnel shape, page-by-page requirements, price ladder, instrumentation blockers, build order, and assumptions to confirm.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional deployment advice may lead users to run a separate funnel builder stack.

Mitigation: Inspect the referenced Autonnel release and docker-compose.yml before running deployment commands.

Risk: Funnel instrumentation can collect tracking identifiers and purchase data.

Mitigation: Collect only the events and identifiers needed for the funnel, and align data capture with the site's privacy terms.

Risk: Benchmark conversion ranges may be mistaken for guaranteed outcomes.

Mitigation: Treat metric ranges as starting benchmarks and replace them with the account's own baseline data.

## Reference(s):

- [Sales Funnel Blueprint on ClawHub](https://clawhub.ai/autonnel/skills/sales-funnel-blueprint)
- [Autonnel Funnel Builder](https://github.com/autonnel/autonnel)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured funnel blueprint with page specs, pricing structure, measurement requirements, build order, and open assumptions.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
