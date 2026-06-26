## Description: <br>
Calls Tencent Cloud OCR QuestionMark Agent APIs to submit K12 exam images or PDFs for asynchronous grading, handwriting recognition, answer analysis, and knowledge-point output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External educators, education platforms, and developers use this skill to submit exam images, PDFs, or single-question images to Tencent Cloud for OCR-based grading, handwriting recognition, answer comparison, and structured analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exam images, PDFs, handwriting, answers, and reference answers may contain student personal information and are submitted to Tencent Cloud for processing. <br>
Mitigation: Install and use only when permitted to send those materials to Tencent Cloud, and redact student personal information where possible. <br>
Risk: The skill requires Tencent Cloud API credentials to submit and poll OCR grading jobs. <br>
Mitigation: Use scoped Tencent Cloud credentials and keep the secret key out of chats, logs, and repositories. <br>


## Reference(s): <br>
- [Tencent Cloud SubmitQuestionMarkAgentJob API](https://cloud.tencent.com/document/api/866/128273) <br>
- [Tencent Cloud DescribeQuestionMarkAgentJob API](https://cloud.tencent.com/document/api/866/128274) <br>
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/tencentcloud-ocr-questionmarkagent) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, guidance] <br>
**Output Format:** [JSON results, with optional raw Tencent Cloud API response output and shell-command usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials and sends user-provided image/PDF content or URLs to Tencent Cloud OCR APIs while polling asynchronous jobs until DONE or FAIL.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
