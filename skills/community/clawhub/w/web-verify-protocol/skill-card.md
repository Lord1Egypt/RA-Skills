## Description:

A three-round web verification protocol that guides agents to grade sources, run independent searches, cross-check data, review narrative numbers, and print a verification report before producing citeable outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyan521](https://clawhub.ai/user/shiyan521)

### License/Terms of Use:

MIT-0

## Use Case:

External writers, analysts, researchers, and content teams use this skill to verify internet-sourced facts and figures before publishing articles, reports, infographics, or business analysis. It is especially suited to tasks where an agent must distinguish official or authoritative sources from low-confidence secondary reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The protocol can slow down simple answers because it requires several independent web searches before producing verified data.

Mitigation: Use it for publishable or decision-relevant facts where stronger verification is worth the added latency.

Risk: The source grading examples are oriented toward Chinese-language and China-focused research contexts.

Mitigation: For other regions or languages, adapt the source grading rules to local official, regulatory, academic, and industry sources before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shiyan521/skills/web-verify-protocol)
- [Publisher profile](https://clawhub.ai/user/shiyan521)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown or text verification reports with source grades and final verified content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires multiple independent web searches and a printed three-round verification report before file output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
