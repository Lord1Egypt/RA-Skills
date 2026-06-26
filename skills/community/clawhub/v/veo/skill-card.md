## Description: <br>
Generate video using Google Veo (Veo 3.1 / Veo 3.0). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buddyh](https://clawhub.ai/user/buddyh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to generate MP4 videos from text prompts, with optional reference images, through Google's Veo/Gemini API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference-image files are sent to Google's Veo/Gemini API. <br>
Mitigation: Use the skill only with prompts and files that are approved for external API processing. <br>
Risk: The optional reference-image path can read and upload a local file selected by the caller. <br>
Mitigation: Do not allow untrusted prompts to choose input-image paths, and verify each path points to a non-sensitive image before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buddyh/veo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Command guidance and status text; generated media is saved as an MP4 file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and GEMINI_API_KEY; optional reference images are read from local file paths.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
