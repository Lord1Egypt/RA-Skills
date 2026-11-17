## Description:

Generates source-grounded vocational education research reports and feasibility analysis reports for single majors or major groups, with Markdown and standalone HTML outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyboat403](https://clawhub.ai/user/flyboat403)

### License/Terms of Use:

MIT-0

## Use Case:

External vocational education administrators, curriculum leads, and professional-program planners use this skill to gather source-backed material, confirm report scope and outline, and produce structured research or feasibility reports for major construction decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTML conversion step may run a locally found script that is not bundled or verified.

Mitigation: Use a bundled, fixed, verified converter or a non-executable conversion path, and fail closed if the expected converter is missing.

Risk: Vocational planning reports could mislead readers if unsupported source material or inferred school facts are presented as established evidence.

Mitigation: Keep source labels on factual claims, preserve explicit unsupported-data markers, and require user confirmation of gathered materials and outlines before drafting.

## Reference(s):

- [Server-resolved GitHub source repository](https://github.com/flyboat403/vocational-report-generator)
- [ClawHub skill page](https://clawhub.ai/flyboat403/skills/vocational-report-generator)
- [Publisher profile](https://clawhub.ai/user/flyboat403)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Guidance, Files]

**Output Format:** [Source-grounded report prose in Markdown plus standalone HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report content is structured by report type and includes source labels, material-confirmation gates, outline confirmation, and explicit markers for unsupported or inferred data.]

## Skill Version(s):

0.1.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
