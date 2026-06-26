## Description: <br>
Manage your ResumeClaw career agent, an AI that represents your professional experience to recruiters, including creating a career agent from a resume, checking recruiter contacts, managing introductions, searching professionals, chatting with candidate agents, and managing notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hherzai-crypto](https://clawhub.ai/user/hherzai-crypto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and recruiting workflows use this skill to manage ResumeClaw career agents from chat, including account access, resume-based agent creation, recruiter introduction decisions, inbox review, agent search, profile review, and notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The search command can run unintended local code. <br>
Mitigation: Avoid the search command until the query/location encoding bug is fixed and review command arguments before execution. <br>
Risk: The skill handles sensitive resume, account, and session data. <br>
Mitigation: Use only trusted ResumeClaw accounts, upload only intended resume text, and remove ~/.resumeclaw/session after use on shared machines. <br>
Risk: Accepting an introduction can exchange contact information. <br>
Mitigation: Explicitly confirm accept or decline actions before running introduction commands. <br>


## Reference(s): <br>
- [ResumeClaw API Reference](references/api.md) <br>
- [ResumeClaw Web App](https://resumeclaw.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/hherzai-crypto/resumeclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with shell command invocations and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands call the ResumeClaw API and store the local session cookie at ~/.resumeclaw/session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
