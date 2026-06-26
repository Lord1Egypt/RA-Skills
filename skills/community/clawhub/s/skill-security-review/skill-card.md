## Description: <br>
Reviews OpenClaw skills or agents before installation or activation, focusing on data exposure, code execution, persistence, network access, privilege escalation, destructive behavior, and supply-chain risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kickook](https://clawhub.ai/user/kickook) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw skills, agents, repositories, archives, or packages before installation, import, activation, or trust decisions. It guides the agent to inspect attack surface, summarize security findings, assign a verdict, and ask for confirmation before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and summarizes untrusted skill artifacts before installation, which may expose sensitive local content if run on broad or unintended paths. <br>
Mitigation: Scope reviews to the intended artifact, inspect compressed or opaque content cautiously, and require a user-visible summary before installation or external action. <br>
Risk: The artifact contains hard-coded user-specific wording that may not fit broad distribution. <br>
Mitigation: Replace user-specific language with neutral wording before publishing or recommending the skill for general use. <br>


## Reference(s): <br>
- [Security Review Checklist](artifact/references/checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kickook/skill-security-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown security audit summary with findings and a decision section] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ALLOW, ALLOW WITH GUARDRAILS, or REJECT verdicts and Low, Medium, High, or Critical risk levels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
