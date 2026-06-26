## Description: <br>
Composes, previews, and sends professional job application emails with resume and cover-letter content through Gmail using the gog tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoxty](https://clawhub.ai/user/xiaoxty) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and job seekers use this skill to prepare, preview, and send personalized job application emails with resume content through Gmail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send job application emails through a Gmail tool, which may expose personal resume information or contact the wrong recipient if details are incorrect. <br>
Mitigation: Verify the recipient, subject, sender account, email body, and resume handling before approving any send. <br>
Risk: Temporary email bodies or job-search logs may contain sensitive personal information. <br>
Mitigation: Remove temporary files or log entries when they are no longer needed, especially on shared systems. <br>
Risk: The workflow depends on a Gmail helper with account access. <br>
Mitigation: Install and use the Gmail helper only when its access requirements are acceptable for the user and environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoxty/resume-email-sender) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with email previews and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated cover-letter text, Gmail send commands, draft fallback guidance, and optional job-search log entries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
