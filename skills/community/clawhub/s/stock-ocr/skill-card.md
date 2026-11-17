## Description:

从通达信金融终端窗口截取股票日K图，并使用OCR识别MA均线数值。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hustjim2026](https://clawhub.ai/user/hustjim2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to capture stock chart regions from the Tongdaxin financial terminal and extract MA moving-average values with OCR. It is intended for workflows that inspect MA5, MA10, MA20, and MA60 values or compare OCR engines for financial chart screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial screenshots may be sent to cloud OCR providers.

Mitigation: Use local OCR where possible, or send screenshots to a cloud OCR provider only after confirming that sharing the image is acceptable.

Risk: OCR credentials appear in the skill evidence and may be reused accidentally.

Mitigation: Rotate or remove embedded OCR credentials and prefer environment variables or a local secret store.

Risk: Setup and PowerShell helper commands can be unsafe when run with untrusted paths, window titles, or pasted credential strings.

Mitigation: Review helper commands before execution and use only trusted input values.

Risk: OCR output can misread market data and produce incorrect moving-average values.

Mitigation: Verify extracted MA values against the trading terminal, especially before using them in financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hustjim2026/skills/stock-ocr)
- [OCR配置指南](artifact/references/ocr_config_guide.md)
- [OCR引擎配置指南](artifact/docs/OCR配置指南.md)
- [Tesseract OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
- [RapidOCR](https://github.com/RapidAI/RapidOCR)
- [Baidu Cloud OCR](https://cloud.baidu.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and OCR result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference screenshot files and OCR engine configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
