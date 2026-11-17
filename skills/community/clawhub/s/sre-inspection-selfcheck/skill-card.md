## Description:

Helps SRE teams assess inspection scripts, scheduled tools, agents, or human-agent workflows against available evidence and independent expectations, then produce a traceable self-check report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thneoly](https://clawhub.ai/user/thneoly)

### License/Terms of Use:

MIT-0

## Use Case:

SRE engineers and developers use this skill to review existing inspection outputs, logs, and expected results, identify evidence gaps, and write a scoped Markdown self-assessment. It supports initial reviews, reanalysis, and comparisons, not independent acceptance or certification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive SRE reports or logs could be shared without authorization.

Mitigation: Use only material you are authorized to share and avoid copying full logs into the report.

Risk: A structural checker result or self-assessment could be mistaken for independent validation or proof of business correctness.

Mitigation: Treat checkers as consistency aids; verify evidence and conclusions independently before acceptance.

Risk: Chinese-language documentation and diagnostics may be difficult for some reviewers to interpret.

Mitigation: Use only when reviewers can understand or reliably translate the source guidance and diagnostics.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/thneoly/skills/sre-inspection-selfcheck)
- [Task recipes](artifact/references/task-recipes.md)
- [Scope and metrics](artifact/references/scope-and-metrics.md)
- [Evidence and truth](artifact/references/evidence-and-truth.md)
- [Sampling guide](artifact/references/sampling-guide.md)
- [Report template](artifact/references/report-template.md)
- [Report consistency](artifact/references/report-consistency.md)
- [NIST proportion intervals](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Markdown self-check report; optional structured summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evidence references, scope limits, missing-data notes, and next steps.]

## Skill Version(s):

1.4.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
