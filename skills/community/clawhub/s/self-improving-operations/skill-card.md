## Description: <br>
Captures process bottlenecks, incident patterns, capacity issues, automation gaps, SLA breaches, and toil accumulation so agents can maintain local operational-learning logs and promote recurring patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operations-focused agents use this skill to capture incidents, reliability patterns, capacity issues, automation gaps, and toil in local markdown logs. Recurring or broadly useful learnings can be promoted into runbooks, postmortems, automation backlogs, capacity models, on-call checklists, or SLO definitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operational-learning logs can accidentally capture sensitive production details such as secrets, customer data, hostnames, internal IPs, or raw command output. <br>
Mitigation: Redact sensitive values before logging, prefer summarized excerpts over raw output, and keep learning files in appropriately scoped workspaces. <br>
Risk: Broad hook activation can add reminders across more projects or prompts than intended. <br>
Mitigation: Prefer project-level hook setup and narrowed matchers; avoid global activation unless cross-project reminders are explicitly desired. <br>
Risk: Automation or remediation ideas recorded by the skill may be incomplete for production use. <br>
Mitigation: Treat remediation examples as design notes until reviewed with explicit approval gates, allowlists, rollback plans, and audit logging. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jose-compu/self-improving-operations) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, reminder text, and shell/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or prompts local .learnings markdown entries; optional hooks emit reminder text and do not modify files directly.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
