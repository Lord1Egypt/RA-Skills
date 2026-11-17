## Description:

Using fixed cameras in multiple zones of a solo-living elder's home, the skill analyzes video streams for human activity and reports a long-term no-activity alert when the configured window, defaulting to 12 hours, is exceeded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External care teams, family caregivers, community elderly-care services, and developers integrating monitoring workflows can use this skill to analyze multi-zone home video for prolonged inactivity indicators and retrieve structured monitoring reports. The skill is an assistive monitoring tool and does not provide medical diagnosis or rescue instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive home-monitoring videos, video URLs, report history, and report export links.

Mitigation: Use it only with informed consent from the monitored person or lawful guardian, confirm the provider's retention policy, and avoid bathrooms or similarly sensitive spaces unless there is a clear legal and privacy basis.

Risk: The skill silently creates or reuses cloud identity state for analysis and history retrieval.

Mitigation: Review identity handling before installation and assume identity values and associated reports may be processed or stored by the provider.

Risk: The skill submits local video files or network video URLs to backend analysis endpoints.

Mitigation: Verify configured endpoints before use and limit submitted media to the intended monitoring scope.

Risk: Long-term inactivity alerts may be incorrect or incomplete because the skill is based on visual activity detection.

Mitigation: Treat alerts as assistive signals and require human verification by phone or in-person check before taking further action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-long-term-immobility-analysis)
- [API documentation](references/api_doc.md)
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown text with structured JSON content and optional report export links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save the returned report text to a local output file when an output path is provided.]

## Skill Version(s):

1.0.10 (source: server release evidence; artifact frontmatter reports 1.0.13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
