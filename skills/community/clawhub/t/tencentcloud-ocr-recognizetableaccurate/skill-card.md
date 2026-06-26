## Description: <br>
Calls Tencent Cloud RecognizeTableAccurateOCR to extract table cells from supported image or PDF inputs and optionally save the recognized table as an Excel file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run Tencent Cloud table OCR on images, PDFs, or URLs when they need structured table text, cell metadata, raw OCR JSON, or an Excel export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected table images, PDFs, or URLs are sent to Tencent Cloud for OCR and may contain sensitive document data. <br>
Mitigation: Process confidential documents only with approval, and use a least-privileged Tencent Cloud OCR key. <br>
Risk: Excel exports may contain sensitive extracted data and can overwrite an existing output file path. <br>
Mitigation: Choose --save-excel paths carefully and handle generated spreadsheets according to the sensitivity of the source document. <br>


## Reference(s): <br>
- [Tencent Cloud RecognizeTableAccurateOCR documentation](https://cloud.tencent.com/document/api/866/86721) <br>
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/tencentcloud-ocr-recognizetableaccurate) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and optional Excel files, with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formatted output includes recognized table count, cell text, coordinates, confidence values, rotation angle, and request ID; raw mode returns Tencent Cloud OCR JSON.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
