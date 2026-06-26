## Description: <br>
Captures finance learnings, operational issues, feature requests, and reminder hooks for reconciliation breaks, forecast variances, control weaknesses, regulatory gaps, valuation errors, and cash flow anomalies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance operators, accountants, auditors, and agent developers use this skill to record anonymized finance issues and recurring process learnings, then promote proven patterns into checklists, controls, procedures, calendars, forecast models, or reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional hooks can run persistently across prompts and sessions, increasing the chance of unwanted reminders or broad finance-log capture. <br>
Mitigation: Use project-level hook configuration, add finance-specific matchers, avoid global user-level hooks, and enable PostToolUse only when detection is needed. <br>
Risk: Finance logs may contain regulated or sensitive business data if entries are copied directly from real workflows. <br>
Mitigation: Anonymize all entries, avoid real account numbers, bank details, client names, taxpayer identifiers, and specific figures, and review logs before sharing or promotion. <br>
Risk: Promoting generated learnings into control matrices, payment workflows, or generated skills could preserve incorrect finance guidance. <br>
Mitigation: Review proposed changes with qualified finance owners before relying on them in close, audit, control, tax, payment, or reporting workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jose-compu/self-improving-finance) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Self-Improving Finance Hook](hooks/openclaw/HOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON hook configuration examples, and markdown log-entry templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated and appended learning entries should be anonymized and reviewed before being promoted into finance procedures or reusable skills.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
