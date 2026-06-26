## Description: <br>
Analyzes sleep-monitoring video to identify sleep stages, body movement, nighttime awakenings, and sleep apnea indicators for sleep quality reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit sleep-monitoring video files or URLs and receive structured sleep quality reports, including stage distribution, movement, awakenings, and apnea indicators. It can also retrieve the user's cloud-hosted historical sleep analysis reports when an open-id is provided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sleep-monitoring videos, remote video URLs, and user identifiers to the publisher's cloud service. <br>
Mitigation: Use only videos and identifiers that are appropriate to share with the publisher's service, and avoid private or unrelated recordings. <br>
Risk: The security summary reports under-disclosed account, token, dependency, and API-scope risks. <br>
Mitigation: Review payment and API-key requirements before use, and deploy only after the publisher resolves the privacy disclosure, token storage behavior, API documentation mismatch, and yaml dependency issue noted by the scan. <br>
Risk: The skill's sleep quality output is for reference and is not a medical diagnosis. <br>
Mitigation: Treat the report as informational guidance and consult qualified medical professionals for diagnosis or treatment decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/smyx-sleep-quality-analysis) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown reports, JSON detail output, and optional saved text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a sleep video file or public video URL and an open-id; supports basic, standard, and JSON detail levels.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
