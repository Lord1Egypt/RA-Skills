## Description: <br>
Telegram-based internal contract generation and eID intake workflow for Vietnamese operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vt-mmm](https://clawhub.ai/user/Vt-mmm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams and developers use this skill to run a Telegram workflow that collects standardized Vietnamese contract data, OCRs eID screenshots on supported macOS hosts, and generates DOCX contracts for internal review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow processes government ID, banking, and contract data and may leave generated DOCX files, downloaded images, mapped JSON, OCR JSON, and state files in the workspace. <br>
Mitigation: Run the skill in a restricted workspace and add a cleanup or retention process for .state, OCR JSON, downloaded images, mapped JSON, and generated DOCX outputs. <br>
Risk: Telegram bot tokens and group chat IDs are required to operate the bot. <br>
Mitigation: Keep tokens and chat IDs outside the packaged skill, protect and rotate the bot token, and use a private contract-only Telegram group. <br>
Risk: The debug OCR flow can expose raw OCR text from eID images in chat. <br>
Mitigation: Avoid debug OCR in shared chats and limit /cccd_debug use to controlled troubleshooting sessions. <br>
Risk: The current OCR path depends on Swift and Apple Vision, so Plan C is not portable unchanged to Linux or Windows. <br>
Mitigation: Use macOS for the bundled OCR path or replace the OCR layer before enabling Plan C on other operating systems. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Vt-mmm/telegram-contract-ops) <br>
- [Architecture](references/architecture.md) <br>
- [Deployment](references/deployment.md) <br>
- [Input Template](references/input-template.md) <br>
- [macOS Runtime Notes](references/macos.md) <br>
- [Windows Runtime Notes](references/windows.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub Publish and Install Notes](references/clawhub.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, Telegram text blocks, JSON OCR data, and DOCX file outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated contracts and OCR artifacts may include personal, banking, and contract data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
