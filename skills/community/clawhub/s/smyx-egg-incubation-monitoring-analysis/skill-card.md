## Description:

Analyzes incubator images of turtle or snake eggs for visible shell, vascular, and embryo changes and produces incubation progress reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Reptile breeders use the skill to review periodic egg images, track visible development signals, and consult incubation progress reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because scanner-reported behavior extends beyond egg monitoring, including remote media analysis, account and credential handling, and an export-only option that may still analyze input.

Mitigation: Treat this as a review-level warning. Before installing, ask the publisher to explain account and credential handling, how remote media is processed, and why export-only may still analyze input.

Risk: Skillspector analysis is incomplete because a referenced local path could not be resolved, leaving some evidence unavailable.

Mitigation: Ask the publisher to clarify the unresolved behavior; the completed AIG scan with no findings does not resolve the reported concerns.

## Reference(s):

- [Egg incubation monitoring API reference](references/api_doc.md)
- [Analysis API reference](skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-egg-incubation-monitoring-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Report links]

**Output Format:** [Structured analysis results and incubation progress reports, with report export links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include development-stage signals, alert levels, and suggested actions.]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata; artifact frontmatter reports 1.0.23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
