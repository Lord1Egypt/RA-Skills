## Description:

Monitors agent skill health with six-dimensional scoring, three alert levels, optimization recommendations, and historical check tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to score individual or grouped agent skills across six health dimensions, surface warning, critical, or emergency states, and generate recommendations before releases or during routine reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The utility stores check history and alerts in memory, so recorded monitoring data is lost when the process restarts.

Mitigation: Export or persist reports externally when historical review is required.

Risk: Health scores depend on caller-provided metrics and can be misleading if inputs are incomplete or subjective.

Mitigation: Validate metric values before invocation and review generated recommendations before acting on them.

Risk: The artifact behaves as a lightweight scoring helper rather than a robust security monitor.

Mitigation: Use explicit invocation and separate security review or scanning before deployment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pagoda111king/skills/skill-health-monitor)
- [Usage Examples](artifact/examples/usage-examples.md)
- [Version History](artifact/VERSION_HISTORY.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown health reports and JavaScript result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language documentation and output examples; scoring depends on caller-provided metric inputs.]

## Skill Version(s):

0.2.0 (source: server release metadata and auto changelog, released 2026-04-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
