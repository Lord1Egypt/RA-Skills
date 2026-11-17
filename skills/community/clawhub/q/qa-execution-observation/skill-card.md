## Description:

Guides QA testers through observing six signals during test execution and recording factual results, outcomes, anomalies, and follow-up items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT

## Use Case:

QA testers and developers use this Chinese-language workflow to observe functional behavior, performance, logs, data, UI, and dependencies while executing test cases, then document actual results and classify anomalies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Log, database, monitoring, or screenshot checks may expose sensitive data or affect systems outside the intended test scope.

Mitigation: Perform these checks only in an authorized test environment and handle captured information appropriately.

Risk: The optional companion installation may introduce code from a separately maintained source.

Mitigation: Install the companion only after verifying that its source and version are trusted.

## Reference(s):

- [Observation guide](references/observation-guide.md)
- [Execution record template](assets/execution-record.md)
- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-execution-observation)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown execution-record tables and per-round observation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves test-case IDs; records observed results, pass/fail/blocked conclusions, signal coverage, and follow-up items.]

## Skill Version(s):

1.8.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
