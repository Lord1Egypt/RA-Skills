## Description:

Receipt Word Tool helps an agent provide a local Tkinter GUI workflow that batch-processes WeChat and Alipay payment screenshots, uses EasyOCR to identify paid amounts, supports manual correction, and generates a formatted Word reimbursement document with thumbnails, subtotals, and totals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gongsunyanming](https://clawhub.ai/user/gongsunyanming)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and operations teams can use this skill to prepare reimbursement records from payment screenshots. Developers and support agents can also use the included guidance to run, maintain, and troubleshoot the local OCR-to-Word workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial screenshots can contain sensitive payment and reimbursement information.

Mitigation: Process screenshots only in trusted local environments and avoid sharing input images or generated documents beyond the reimbursement workflow.

Risk: The bundled model download guidance uses weak verification for OCR model files, including a curl option that reduces certificate revocation checking.

Mitigation: Prefer verified model sources, pinned versions, and SHA-256 checks; avoid --ssl-no-revoke unless the operator understands and accepts the reduced protection.

Risk: OCR-extracted amounts may be incorrect and could affect reimbursement totals.

Mitigation: Manually review and correct recognized amounts before generating or submitting the Word reimbursement document.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gongsunyanming/skills/yiqi-receipt-word-tool)
- [EasyOCR Offline Setup](references/easyocr_offline_setup.md)
- [Maintenance Guide](references/maintenance_guide.md)
- [EasyOCR CRAFT Detection Model](https://modelscope.cn/models/ms-agent/craft_mlt_25k/resolve/master/craft_mlt_25k.zip)
- [EasyOCR Chinese Recognition Model](https://modelscope.cn/models/ms-agent/zh_sim_g2/resolve/master/zh_sim_g2.zip)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python GUI source, shell commands, configuration notes, and a generated DOCX workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local tool processes image files and produces a Word document containing screenshots, recognized or corrected amounts, subtotals, and a total.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
