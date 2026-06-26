## Description: <br>
Summarizes Enterprise WeChat group or direct messages, extracting key points, action items, risks, and decisions into readable daily reports, weekly reports, or meeting notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dymdsunp-dot](https://clawhub.ai/user/dymdsunp-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to turn Enterprise WeChat conversation text, OCR text from screenshots, or selected message excerpts into concise workplace summaries with progress, risks, decisions, action items, and missing information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste sensitive workplace messages, secrets, or unnecessary personal details into the summarization prompt. <br>
Mitigation: Use the smallest necessary message range, remove secrets and unnecessary personal details before sharing content or OCR text, and review the summary before forwarding it. <br>
Risk: The summary may overstate conclusions when the supplied conversation excerpt is incomplete or ambiguous. <br>
Mitigation: Preserve the skill behavior of marking unsupported conclusions as insufficient information and listing important missing details for confirmation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown structured summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include a one-sentence overview, key progress, risks, decisions, action items with owners and due dates when available, and up to three items needing confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
