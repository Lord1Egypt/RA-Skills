## Description: <br>
Vision Sandbox sends an image and prompt to Gemini with code execution enabled for spatial grounding, visual math, and UI auditing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johanesalxd](https://clawhub.ai/user/johanesalxd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding agents use Vision Sandbox to analyze screenshots and images, returning grounded observations such as coordinates, counts, layout issues, generated code, and model reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, screenshots, prompts, and resulting analysis are sent to Google Gemini under the user's API key. <br>
Mitigation: Avoid submitting secrets, credentials, private customer data, or confidential screenshots unless permitted by the user's data-handling policy; use a constrained or monitored Gemini key where possible. <br>
Risk: Vision analysis and generated sandbox code may produce incorrect coordinates, counts, or layout conclusions. <br>
Mitigation: Review model responses and code execution output before applying results to user-facing interfaces or automated changes. <br>


## Reference(s): <br>
- [Vision Sandbox on ClawHub](https://clawhub.ai/johanesalxd/vision-sandbox) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown-style terminal output with model text, fenced Python code, code execution output, and optional generated image file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and GEMINI_API_KEY; may write sandbox_output PNG files when Gemini returns inline media.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
