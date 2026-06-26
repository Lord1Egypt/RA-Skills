## Description: <br>
Monitors plant images or videos for early wilting signs, suspected causes, severity, early warning status, and management guidance using a remote SMYX/LifeEmergence analysis service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze plant media for early wilting, distinguish environmental stress from possible pathological wilt, and retrieve previous monitoring reports. The output is intended as an early warning aid and should be checked against field conditions and expert judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded plant images or videos, URLs, usernames, phone numbers, open-id values, and stored tokens may leave the device or persist locally. <br>
Mitigation: Use non-sensitive media, avoid private locations or people in test data, provide a dedicated non-secret user identifier, and treat remote service use as external data processing. <br>
Risk: The skill requires a paid service or sensitive credentials and silently handles account login, registration, and local tokens. <br>
Mitigation: Install only when the publisher and remote LifeEmergence/SMYX services are trusted, verify dependencies before installation, do not use an API key as a user identifier, and remove or rotate tokens when no longer needed. <br>
Risk: The security summary says parts of the package do not match the advertised plant-only purpose. <br>
Mitigation: Review the package scope before deployment and restrict use to the documented plant wilting monitoring workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-plant-wilting-monitoring-analysis) <br>
- [API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Network video analysis demo](https://www.coze.cn/s/YIgTq0_VqGw/) <br>
- [Uploaded video analysis demo](https://www.coze.cn/s/7wcbssKiNKI/) <br>
- [Historical report demo](https://www.coze.cn/s/zdWebDlpbZo/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or JSON text with structured analysis results, report lists, and report export links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote report URLs and optional output files when requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
