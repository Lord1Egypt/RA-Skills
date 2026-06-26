## Description: <br>
Run overnight skill health reviews, replay-case availability checks, feedback triage, and proposal-only maintenance reports for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheepxux](https://clawhub.ai/user/sheepxux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use Somnia to schedule quiet-hour reviews of OpenClaw skills, summarize health findings, check feedback and replay-case availability, and create proposal artifacts before any update decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scheduler can create persistent local background runs. <br>
Mitigation: Review the generated plist before using --apply and install only when a local nightly scheduler is intended. <br>
Risk: A user-specified plist path can be removed when uninstall is applied. <br>
Mitigation: Avoid custom --plist values unless you intend Somnia to manage that exact file. <br>
Risk: Telegram reports may share skill names and health summaries outside the local machine. <br>
Mitigation: Enable Telegram reporting only for chats where those summaries are acceptable to share. <br>


## Reference(s): <br>
- [Somnia Architecture](references/somnia-architecture.md) <br>
- [Schedule And Policy](references/schedule-and-policy.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sheepxux/somnia) <br>
- [Publisher Profile](https://clawhub.ai/user/sheepxux) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON reports, proposal files, scheduler configuration, and concise user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local health reports and proposal artifacts; Telegram reporting is optional when configured.] <br>

## Skill Version(s): <br>
0.4.3 (source: server release evidence and SKILL.md overview) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
