## Description: <br>
Skin Disease Analysis - Analyze skin photos through local file binary upload and identify possible conditions via WiseDiag AI when the user provides a local image file path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wisediag](https://clawhub.ai/user/wisediag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to analyze local skin image files with WiseDiag AI and receive possible condition analysis and recommendations. It is intended for reference support only, not medical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skin photos may contain sensitive health or identifying information and are sent to WiseDiag's cloud service for processing. <br>
Mitigation: Upload only images the user is comfortable transmitting, avoid identifiable or intimate images unless consent is clear, and confirm trust in WiseDiag's data handling before use. <br>
Risk: The WISEDIAG_API_KEY is a sensitive credential required by the skill. <br>
Mitigation: Store the API key in the environment, avoid printing or committing it, and rotate it if it may have been exposed. <br>
Risk: Generated analysis reports are saved locally and may contain sensitive health information. <br>
Mitigation: Protect or delete reports from ~/.openclaw/workspace/WiseDiag-Skin when they are no longer needed. <br>
Risk: The analysis can be mistaken for medical diagnosis or treatment advice. <br>
Mitigation: Treat outputs as reference information only and consult a qualified healthcare professional for health concerns. <br>


## Reference(s): <br>
- [WiseDiag-Skin on ClawHub](https://clawhub.ai/wisediag/wisediag-skin) <br>
- [WiseDiag API key console](https://console.wisediag.com/apiKeyManage) <br>
- [WiseDiag OpenAPI service](https://openapi.wisediag.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Streaming terminal text plus a saved Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WISEDIAG_API_KEY and a local image file path; saves reports to ~/.openclaw/workspace/WiseDiag-Skin by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
