## Description: <br>
Receipt Word Tool is a local GUI utility that batch-processes WeChat and Alipay payment screenshots, uses EasyOCR to identify paid amounts, supports manual corrections, and generates a formatted Word reimbursement document with thumbnails, subtotals, and a total. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongsunyanming](https://clawhub.ai/user/gongsunyanming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users can use this skill to process batches of payment screenshots into reimbursement-ready Word documents. The workflow is intended for local OCR extraction, manual review of amounts, and formatted document generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR can misread receipt amounts and affect reimbursement totals. <br>
Mitigation: Review and correct the detected amounts before using the generated Word document for reimbursement. <br>
Risk: EasyOCR model setup may download model files, and the offline guide includes a reduced certificate-checking curl option. <br>
Mitigation: Prefer normal TLS downloads or verified offline model files; use reduced certificate checking only when the operational risk is understood. <br>
Risk: The generated Word document may be opened automatically by the local operating system. <br>
Mitigation: Run the tool only on intended local image folders and confirm the output path before generation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gongsunyanming/yiqi-receipt-word-tool) <br>
- [EasyOCR Offline Setup](references/easyocr_offline_setup.md) <br>
- [Maintenance Guide](references/maintenance_guide.md) <br>
- [EasyOCR Detection Model](https://modelscope.cn/models/ms-agent/craft_mlt_25k/resolve/master/craft_mlt_25k.zip) <br>
- [EasyOCR Chinese Recognition Model](https://modelscope.cn/models/ms-agent/zh_sim_g2/resolve/master/zh_sim_g2.zip) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Python GUI tool that generates DOCX files and supporting Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local image files and produces a Word document with thumbnails, OCR-derived amounts, subtotals, and a final total.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
