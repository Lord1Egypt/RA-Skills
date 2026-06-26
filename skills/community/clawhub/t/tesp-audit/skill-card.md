## Description: <br>
Audits whether the Task Execution Signal Protocol is still being followed through low-token, exception-first checks for version drift, queue hygiene, numeric stage format, and core execution anchors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wewehg](https://clawhub.ai/user/wewehg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leads, and governance reviewers use this skill to check whether a workspace still follows the current TESP baseline, including file anchors, visible versions, numeric progress notation, active-board hygiene, and archive handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may audit the wrong workspace or write a local report somewhere unexpected. <br>
Mitigation: Confirm the workspace scope and report destination before installation or use. <br>


## Reference(s): <br>
- [TESP Audit Reference](references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wewehg/tesp-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise Markdown or plain-text exception report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exception-first output; normal audits may write a short local report and avoid proactive chat messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
