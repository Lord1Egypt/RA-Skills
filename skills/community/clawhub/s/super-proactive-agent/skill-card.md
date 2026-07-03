## Description: <br>
A proactive-agent skill that gives AI agents patterns and templates for persistent memory, proactive check-ins, onboarding, self-improvement, and security auditing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure AI agents that retain durable work context, recover from compaction, perform proactive follow-up, and maintain guardrails around external actions and security-sensitive behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable personal or work memory can accumulate sensitive context without a clear review path. <br>
Mitigation: Require explicit opt-in for memory files, define what may be stored, and add a recurring review and delete process for all memory artifacts. <br>
Risk: Proactive monitoring can affect email, calendar, browser, screenshots, cron jobs, sub-agents, BOOTSTRAP.md handling, or self-modifying operating files without enough user control. <br>
Mitigation: Edit the rules before use so each of those behaviors requires clear user approval and has a visible audit trail. <br>
Risk: Background crons and autonomous sub-agents may perform work outside the main conversation. <br>
Mitigation: Limit autonomous jobs to low-risk checks, require human approval before external or destructive actions, and review cron prompts and outputs regularly. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/super-proactive-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/subaru0573) <br>
- [Onboarding Flow Reference](artifact/references/onboarding-flow.md) <br>
- [Security Patterns Reference](artifact/references/security-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with template files and shell script examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operating rules, memory templates, onboarding prompts, heartbeat checklists, and a security audit script for an agent workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
