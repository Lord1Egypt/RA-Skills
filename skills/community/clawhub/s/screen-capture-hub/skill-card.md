## Description: <br>
A screen capture, OCR, and screen analysis skill for AI assistants that can capture full-screen or regional screenshots, extract Chinese and English text, and run basic image analysis workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datappt8](https://clawhub.ai/user/datappt8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation builders, and AI assistant operators use this skill to capture screen images, extract visible text with OCR, and analyze screen content such as text, colors, and edges. It is intended for workflows where screen content must be inspected or saved through Python command-line tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture sensitive screen contents and save screenshots, OCR text, or logs to disk. <br>
Mitigation: Install only from a trusted publisher, use explicit capture regions and output paths where possible, and delete saved screenshots, OCR text, and logs that may contain sensitive information. <br>
Risk: The Windows OCR installer flow can download and silently run an external Tesseract installer without integrity verification. <br>
Mitigation: Prefer manual, verified Tesseract installation from trusted sources and avoid running installer scripts as administrator unless required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/datappt8/screen-capture-hub) <br>
- [Publisher Profile](https://clawhub.ai/user/datappt8) <br>
- [Usage Examples](references/usage_examples.md) <br>
- [Tesseract OCR Setup Guide](docs/OCR_SETUP_GUIDE.md) <br>
- [Tesseract OCR Documentation](https://tesseract-ocr.github.io/) <br>
- [UB Mannheim Tesseract Windows Builds](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, image files, text files, and JSON analysis outputs produced by the skill scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Screen capture outputs may include PNG image files, OCR text files, and JSON reports depending on the selected script and command-line options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json, CHANGELOG released 2026-03-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
