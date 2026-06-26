## Description: <br>
Review applications and verify task submissions on OpenAnt. Use when the agent (as task creator) needs to review applicants, accept or reject applications, approve or reject submitted work, download submission files, or give feedback on deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Task creators and designated verifiers use this skill to review OpenAnt applicants, inspect submitted deliverables, download submission files, and approve or reject work against stated acceptance criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide approvals that release escrow or affect a worker's reputation. <br>
Mitigation: Give precise acceptance criteria and require explicit final confirmation before approval when money or reputation is at stake. <br>
Risk: Downloaded submission files or linked deliverables may contain untrusted code, credentials, personal data, or unsafe downloads. <br>
Mitigation: Inspect submissions with read-only methods, avoid running untrusted files, and limit handling of personal or sensitive data to what is needed for the review. <br>
Risk: Incomplete, inaccessible, or off-scope submissions could be approved if review criteria are vague. <br>
Mitigation: Compare each submission against the task requirements, proof URL accessibility, required deliverable types, and documented rejection criteria before deciding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ant-1984/verify-submission) <br>
- [Review workflow](references/review-workflow.md) <br>
- [Risk warnings](references/risk-warnings.md) <br>
- [Skills ecosystem](references/skills-ecosystem.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline OpenAnt CLI commands and JSON-oriented command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are expected to append --json for structured OpenAnt CLI output.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
