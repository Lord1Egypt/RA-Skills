## Description: <br>
Detects and analyzes indoor plant light stress from plant images or videos, optionally combined with lux data, to identify insufficient, excessive, or normal light conditions and suggest care adjustments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and plant-care developers use this skill to analyze indoor plant images, videos, or public image URLs for light stress symptoms and receive structured care guidance. It also supports querying cloud-hosted historical reports associated with the service-managed identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends submitted plant images, videos, or URLs to external cloud services for analysis. <br>
Mitigation: Avoid submitting private images, internal URLs, or sensitive workspace files unless the user trusts the service and its data handling. <br>
Risk: The skill may automatically create or reuse a service identity and store access tokens in the workspace. <br>
Mitigation: Use a dedicated workspace for this skill and review or clear locally stored service credentials when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-indoor-plant-light-stress-detect-analysis) <br>
- [API Documentation](references/api_doc.md) <br>
- [Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON structured analysis report, with optional report export links and command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write analysis output to a user-selected file path when the output option is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
