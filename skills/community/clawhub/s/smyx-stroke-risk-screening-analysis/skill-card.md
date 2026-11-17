## Description:

Combines facial feature recognition with physiological indicators to provide stroke-risk screening reports and related guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Intended for people seeking an initial stroke-risk screening based on facial images or video and optional physiological indicators. It returns a structured report with risk prompts and lifestyle or care-seeking guidance; the skill states that this does not replace medical examination or diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because scanners report a mismatch with its stated stroke-screening purpose and concerns about remote handling of sensitive information.

Mitigation: Clarify the skill's purpose and data handling before installation; do not send identifiable face media or health indicators unless the remote service and its handling are trusted.

Risk: The security summary flags undeclared account and file side effects.

Mitigation: Review account initialization and file behavior before running, and use only media you are authorized to process.

Risk: Skillspector reports partial coverage because a referenced local path was missing, so unreported behavior is not confirmed safe.

Mitigation: Review the full release contents and its data flows before installation.

Risk: A screening report could be mistaken for a medical diagnosis.

Mitigation: Treat results as screening prompts only and seek qualified medical care for concerning symptoms or findings.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-stroke-risk-screening-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API reference included with the skill](references/api_doc.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown, Guidance]

**Output Format:** [Structured screening report, JSON by default; concise or detailed text and Markdown report lists are also described.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk indicators, lifestyle or medical guidance, and report links; results depend on a remote service.]

## Skill Version(s):

1.0.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
