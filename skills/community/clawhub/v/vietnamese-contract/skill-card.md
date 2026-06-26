## Description: <br>
Helps agents draft Vietnamese legal contracts and related agreements, verify legal bases, format professional .docx files, run Vietnamese spell checks, and optionally extract ID-card details with OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trustydev212](https://clawhub.ai/user/trustydev212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Vietnamese-speaking users and document-preparation agents use this skill to collect contract details, draft Vietnamese legal documents, generate .docx outputs, and validate formatting and spelling before delivery. <br>

### Deployment Geography for Use: <br>
Global (focused on Vietnamese legal-document workflows) <br>

## Known Risks and Mitigations: <br>
Risk: The optional CCCD/CMND OCR workflow can process sensitive identity data. <br>
Mitigation: Use OCR only when needed, avoid real ID images where possible, confirm before sending extracted text to an AI model, and delete temporary identity data after contract generation. <br>
Risk: Generated Vietnamese legal documents may contain outdated legal bases or terms that are not appropriate for the user's situation. <br>
Mitigation: Verify current Vietnamese legal sources before relying on the draft and have important or complex contracts reviewed by a qualified lawyer. <br>
Risk: OCR output may misread names, dates, addresses, or ID numbers. <br>
Mitigation: Show extracted fields to the user for confirmation and mark uncertain values for manual correction before inserting them into a contract. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trustydev212/vietnamese-contract) <br>
- [OpenClaw Viet Nam community](https://zalo.me/g/lajsqc334jqc5fezevvo) <br>
- [CCCD OCR guide](references/cccd-ocr-guide.md) <br>
- [Contract structures](references/contract-structures.md) <br>
- [DOCX formatting](references/docx-formatting.md) <br>
- [Legal bases](references/legal-bases.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell, Python, and JavaScript snippets plus generated .docx documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and pandoc for the core workflow; optional CCCD OCR uses EasyOCR and OpenCV.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
