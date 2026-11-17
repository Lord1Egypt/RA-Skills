## Description:

TencentCloud QuestionMark OCR submits K12 exam images or PDFs to Tencent Cloud OCR for asynchronous grading, handwritten answer recognition, answer analysis, knowledge point extraction, and structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and education workflow builders use this skill to submit K12 exam images or PDFs for automated grading and OCR-based analysis through Tencent Cloud. The skill returns structured results for review or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exam images, PDFs, handwritten answers, and related results are sent to Tencent Cloud for OCR and marking.

Mitigation: Install and use the skill only when that external processing is intended, and confirm permission to process any student or personal data through Tencent Cloud.

Risk: The script requires Tencent Cloud API credentials in environment variables.

Mitigation: Use Tencent Cloud credentials with the minimum permissions needed and avoid shared environments for secrets.

Risk: Automated OCR and grading results can affect education workflows if used without review.

Mitigation: Review the structured grading results before relying on them in assessment, reporting, or student-facing workflows.

## Reference(s):

- [Tencent Cloud SubmitQuestionMarkAgentJob API documentation](https://cloud.tencent.com/document/api/866/128273)
- [Tencent Cloud DescribeQuestionMarkAgentJob API documentation](https://cloud.tencent.com/document/api/866/128274)
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/skills/tencentcloud-ocr-questionmarkagent)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON results with Markdown guidance and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports formatted Chinese JSON output by default and raw Tencent Cloud API JSON when requested.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
