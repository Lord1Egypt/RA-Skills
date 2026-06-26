## Description: <br>
Generates condensed album highlights by extracting video segments that match user-specified keywords or target subjects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit local or network video inputs, specify target people, pets, scenes, or events, and receive a condensed time-lapse album analysis or report history from the cloud service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video inputs, URLs, report history, and account identifiers are sent to and may be stored by the configured cloud analysis service. <br>
Mitigation: Use only non-sensitive footage and non-phone open-id values, and obtain explicit consent before uploading personal videos or querying stored reports. <br>
Risk: The security review flags under-disclosed account login/registration, local token storage, and broad report/API access. <br>
Mitigation: Review the skill before installation, document account and token handling, and prefer a release that removes unused mutation APIs. <br>
Risk: The bundled shared code and references include confusing health-analysis behavior that may not match the time-lapse album purpose. <br>
Mitigation: Limit use to the documented custom time-lapse analysis workflow and verify outputs before relying on them. <br>


## Reference(s): <br>
- [Skill API documentation](references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-custom-timelapse-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-style analysis results, including report-history tables with links when listing prior reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an open-id and sends video inputs or URLs to the configured cloud analysis service.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
