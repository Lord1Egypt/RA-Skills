## Description: <br>
Batch uploads user-provided content or Markdown-formatted posts into the Toutiao micro-headline draft box with optional images and automatic draft saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanlvxu](https://clawhub.ai/user/tanlvxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators with an already logged-in Toutiao creator session use this skill to turn batches of direct text or Markdown into saved micro-headline drafts, including optional image upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a logged-in Toutiao creator session and may save drafts to the wrong account if the active session is not checked. <br>
Mitigation: Confirm the active Toutiao account and intended content batch before running the upload workflow. <br>
Risk: Image links from untrusted sources may download unwanted content or leave staged files behind. <br>
Mitigation: Use trusted image URLs, review downloaded files before upload when possible, and clean up staged files after the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tanlvxu/toutiaodraft) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Browser actions, Files] <br>
**Output Format:** [Markdown instructions with browser automation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download temporary image files before uploading them to a logged-in Toutiao draft workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
