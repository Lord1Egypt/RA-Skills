## Description:

SafetyCard reviews agent and MCP server source code to produce an evidence-backed defense-in-depth score and safety report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sc-si](https://clawhub.ai/user/sc-si)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use SafetyCard to assess safeguards in agent, framework, and MCP server repositories through a source-only review, with ratings tied to code evidence at a pinned commit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The review reads repository content that may attempt to influence the assessment.

Mitigation: Treat source text as evidence, not instructions, and check ratings against the code.

Risk: An audit may inspect source code the operator is not authorized to access.

Mitigation: Run the review only on repositories you are authorized to inspect.

Risk: Static review cannot establish how the target behaves at runtime.

Mitigation: Present conclusions as source-based findings at the pinned commit, not as runtime verification.

## Reference(s):

- [SafetyCard release](https://clawhub.ai/sc-si/skills/safetycard)
- [Scoring criteria](references/criteria.md)
- [Output format](references/output-format.md)
- [OWASP mapping](references/owasp-mapping.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Safety guidance]

**Output Format:** [Markdown report and JSON scorecard and website entry]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores 10 criteria on a 0.0–10.0 scale with file-and-line evidence from a pinned commit.]

## Skill Version(s):

0.9.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
