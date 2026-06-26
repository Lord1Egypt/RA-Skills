## Description: <br>
Captures pipeline leaks, objection patterns, pricing errors, forecast misses, competitor shifts, and deal velocity drops to enable continuous sales improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams and agent users use this skill to capture recurring sales issues, deal learnings, and feature requests, then promote validated patterns into battle cards, objection handling scripts, pricing playbooks, or qualification frameworks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive sales context in learning logs, including customer information, pricing, contract terms, or strategy if users do not redact entries. <br>
Mitigation: Use project-local setup, keep .learnings/ out of shared repositories unless reviewed, and redact customer names, exact quotes, transcript excerpts, pricing, contract terms, and strategy before storing or sharing entries. <br>
Risk: Broad prompt hooks may add reminders outside the intended sales workflow. <br>
Mitigation: Use the provided sales-specific matcher instead of empty matchers, avoid global hooks, and enable optional hooks only where sales-learning reminders are desired. <br>


## Reference(s): <br>
- [Self-Improving Sales on ClawHub](https://clawhub.ai/jose-compu/self-improving-sales) <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [Hooks Setup](artifact/references/hooks-setup.md) <br>
- [Examples](artifact/references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured log-entry templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates project-local learning logs when the agent follows the workflow; optional hooks inject reminder text during agent bootstrap or prompt submission.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
