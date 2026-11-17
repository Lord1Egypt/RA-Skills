## Description:

Calls Tencent Cloud RecognizeTableAccurateOCR to extract table structure, cell text, coordinates, confidence scores, rotation angle, and optional Excel data from supported image or single-page PDF inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tencent Cloud table OCR on images or PDFs when they need structured table text, table geometry, confidence values, and optional Excel export data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected image or PDF content, or a URL to that content, to Tencent Cloud for OCR processing.

Mitigation: Use only documents approved for Tencent Cloud processing and avoid submitting sensitive content without the required data handling approval.

Risk: The skill requires Tencent Cloud API credentials through environment variables.

Mitigation: Use narrowly scoped Tencent Cloud credentials, rotate them regularly, and run the skill in an isolated environment.

Risk: The script depends on the Tencent Cloud Python SDK being installed at runtime.

Mitigation: Install the SDK in a controlled environment and prefer a pinned dependency version.

## Reference(s):

- [Tencent Cloud RecognizeTableAccurateOCR documentation](https://cloud.tencent.com/document/api/866/86721)
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/skills/tencentcloud-ocr-recognizetableaccurate)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [JSON OCR results printed to stdout, with optional Base64-decoded Excel file output when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud OCR credentials and either an image/PDF URL or Base64/file input; formatted output is the default and raw API JSON is available with --raw.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
