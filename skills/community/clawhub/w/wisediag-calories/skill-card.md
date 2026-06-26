## Description: <br>
Food Calorie Estimator — Identify food items and estimate calories from an image via local file binary upload or image URL with AI-powered recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wisediag](https://clawhub.ai/user/wisediag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to estimate food calories and nutrition details from user-selected food photos or image URLs. It is intended for reference analysis only and is not a substitute for professional nutrition or dietary advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected food photos, image URLs, and related question text are sent to WiseDiag cloud servers for processing. <br>
Mitigation: Use the skill only with images and questions suitable for remote processing, and avoid content with private people, documents, locations, or other sensitive background details. <br>
Risk: The skill requires a WiseDiag API key. <br>
Mitigation: Prefer a temporary environment variable or a dedicated secret manager, and avoid permanently adding the key to shell startup files. <br>
Risk: Calorie and nutrition output may be imprecise and is not professional advice. <br>
Mitigation: Treat results as reference information and consult a qualified nutrition professional for dietary decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wisediag/wisediag-calories) <br>
- [WiseDiag Calories homepage](https://github.com/wisediag/WiseDiag-Calories) <br>
- [WiseDiag API key management](https://console.wisediag.com/apiKeyManage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal streaming text and saved Markdown files with optional JSON detection details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are saved locally as Markdown under the configured output directory, defaulting to ~/.openclaw/workspace/WiseDiag-Calories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
