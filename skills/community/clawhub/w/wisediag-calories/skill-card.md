## Description:

WiseDiag-Calories estimates food calories and nutritional content from user-provided food images using local file upload or image URL analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wisediag](https://clawhub.ai/user/wisediag)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze food photos or image URLs, ask calorie-related questions, and receive a saved Markdown report with estimated calories and nutrition details. It is for reference only and is not a substitute for professional nutritional advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected food photos, image URLs, questions, and related metadata to WiseDiag cloud services for analysis.

Mitigation: Use only with images appropriate for remote processing and avoid uploading private or sensitive content.

Risk: The skill requires a WiseDiag API key for requests.

Mitigation: Store the API key in a temporary environment variable or credential manager and avoid committing it to files.

Risk: Calorie and nutrition estimates may be inaccurate or incomplete.

Mitigation: Treat outputs as reference information and consult a qualified nutrition professional for dietary decisions.

Risk: Custom output filename handling has a hardening caveat in the security guidance.

Mitigation: Prefer simple filename stems until output-name validation is tightened.

## Reference(s):

- [WiseDiag-Calories ClawHub listing](https://clawhub.ai/wisediag/skills/wisediag-calories)
- [WiseDiag publisher profile](https://clawhub.ai/user/wisediag)
- [WiseDiag API key management](https://console.wisediag.com/apiKeyManage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with streaming terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WISEDIAG_API_KEY; accepts up to 5 local image files or image URLs and saves results as a Markdown file.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
