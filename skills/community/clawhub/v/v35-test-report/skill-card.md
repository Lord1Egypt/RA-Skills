## Description:

Analyzes v3.5 production deployment logs and generates test report statistics for run counts, v3.5 versus v3.0 comparisons, prediction accuracy, and strategy analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rf-ai-wh](https://clawhub.ai/user/rf-ai-wh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to summarize a local v3.5 production deployment log, compare v3.5 and v3.0 performance, and prepare concise test-report statistics for AI agent evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fixed local log path may contain secrets, user data, internal identifiers, or sensitive operational details.

Mitigation: Confirm /tmp/agent_v35_production.log is the intended input and sanitize sensitive data before running the report.

Risk: The skill may be expected to provide monitoring, visualizations, strategy analytics, or exported files beyond its actual behavior.

Mitigation: Use it as a local console summary tool for aggregate statistics, and validate whether additional reporting or monitoring is needed separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rf-ai-wh/skills/v35-test-report)
- [Publisher profile](https://clawhub.ai/user/rf-ai-wh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and console text report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads /tmp/agent_v35_production.log and prints aggregate statistics; it does not export report files.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
