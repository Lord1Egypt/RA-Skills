## Description: <br>
Automates Tsinghua Learn tasks including login, todo review, courseware downloads, homework submission, PDF preparation, and marking course items as read. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomuiv](https://clawhub.ai/user/tomuiv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students or authorized users with Tsinghua Learn accounts use this skill to manage routine coursework tasks, such as checking todos, downloading materials, submitting homework, and reviewing course updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable local login material, including credentials, browser profile state, and session data. <br>
Mitigation: Install only on a trusted Windows machine, treat stored account state as sensitive, and use the reset flow when local account state should be removed. <br>
Risk: The skill can mark course announcements or materials as read during normal coursework management. <br>
Mitigation: Review or disable auto_mark_read before routine use if todo checks should remain read-only. <br>
Risk: Homework submission is a high-impact action for the user. <br>
Mitigation: Review the submission preview before confirming and verify important submissions on the official Tsinghua Learn site. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomuiv/tsinghua-learn) <br>
- [Tsinghua Learn](https://learn.tsinghua.edu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Conversational Markdown with JSON-backed status summaries and generated local files when downloading, merging PDFs, or preparing homework submissions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows and a Tsinghua Learn credential supplied through CAS_PASSWORD.] <br>

## Skill Version(s): <br>
1.0.17 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
