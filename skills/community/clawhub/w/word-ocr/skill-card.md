## Description: <br>
OCR and text extraction from Word documents (.docx, .doc) using the MinerU API, including scanned Word documents, image-based Word files, embedded images, quick OCR, and advanced OCR with table and formula recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veeicwgy](https://clawhub.ai/user/veeicwgy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing users use this skill to extract text from scanned, image-heavy, or legacy Word documents and to choose the appropriate MinerU OCR command for quick or higher-precision extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Word documents may be processed by MinerU's external CLI/API, creating privacy considerations for confidential, regulated, client, or personal documents. <br>
Mitigation: Use only documents approved for external OCR processing and follow the security guidance before uploading or extracting sensitive content. <br>
Risk: Advanced OCR extraction can require a MinerU token. <br>
Mitigation: Protect the token and configure it only when precision OCR, table recognition, or formula detection is needed. <br>


## Reference(s): <br>
- [MinerU API token management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for MinerU CLI output directories and may result in extracted text or document output files.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
