## Description: <br>
Generate professional PowerPoint presentations from text manuscripts and style examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loommo](https://clawhub.ai/user/loommo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees and business users use this skill to turn manuscripts, work reports, and style examples into editable PowerPoint presentations with HTML preview, image handling, and optional AI illustrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User manuscripts, screenshots, or style examples may be sent to the configured LLM or image generation provider. <br>
Mitigation: Confirm the configured provider and data-handling policy before using confidential material. <br>
Risk: Optional AI illustration generation depends on nanobanana-skill and a Gemini API key. <br>
Mitigation: Review and configure that dependency separately before enabling AI illustrations. <br>
Risk: Untrusted image URLs can introduce external content or outbound requests during presentation generation. <br>
Mitigation: Prefer trusted local images or run in an environment that restricts outbound requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/loommo/report-ppt-generator-pro) <br>
- [Style Extraction](references/style-extraction.md) <br>
- [Image Handling](references/image-handling.md) <br>
- [Work Report Layouts](references/work-report-layouts.md) <br>
- [AI Illustration Prompts](references/ai-illustration-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON snippets, HTML/CSS templates, JavaScript conversion code, shell commands, and generated HTML/PPTX file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce HTML slide previews, editable PPTX files, and optional AI illustration prompts or image assets.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence; artifact/package.json reports 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
