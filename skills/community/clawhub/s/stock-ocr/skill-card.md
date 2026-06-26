## Description: <br>
从通达信金融终端窗口截取股票日K图，并使用OCR识别MA均线数值。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hustjim2026](https://clawhub.ai/user/hustjim2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect a Windows stock trading terminal, capture the moving-average area of a daily K-line chart, and extract MA values with OCR. It is intended for chart-reading automation, not as investment advice or unattended trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can focus and type into a live trading application window. <br>
Mitigation: Verify the exact target window title before execution and avoid running it while order-entry or unrelated sensitive windows are active. <br>
Risk: Screenshots of financial charts may be saved locally or sent to cloud OCR services. <br>
Mitigation: Prefer local OCR for sensitive workflows, avoid visible confidential content, and delete retained screenshots when they are no longer needed. <br>
Risk: Embedded or configured OCR credentials may be exposed or reused. <br>
Mitigation: Remove embedded credentials, rotate any exposed keys, and provide OCR credentials through user-controlled environment variables or local secret storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hustjim2026/stock-ocr) <br>
- [OCR配置指南](docs/OCR配置指南.md) <br>
- [OCR configuration reference](references/ocr_config_guide.md) <br>
- [Baidu Cloud OCR](https://cloud.baidu.com/) <br>
- [RapidOCR](https://github.com/RapidAI/RapidOCR) <br>
- [Tesseract OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and OCR-extracted numeric values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local screenshot files when requested; OCR accuracy depends on chart visibility, OCR engine, and credential configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
