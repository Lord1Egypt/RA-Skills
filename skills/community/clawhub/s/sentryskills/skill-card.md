## Description: <br>
SentrySkills is an automatic local security guard for agents that checks prompts, runtime actions, and final responses for prompt injection, data leaks, unsafe commands, and code vulnerabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengbiaojie](https://clawhub.ai/user/zengbiaojie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use SentrySkills to add local preflight, runtime, and output checks around agent tasks that involve shell commands, file changes, sensitive context, external tools, or code generation. It is intended to support safer agent operation through configurable policy profiles, event logs, and allow, downgrade, or block decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently influence every agent response when automatic mode is enabled. <br>
Mitigation: Review and manually merge AGENTS.md changes, confirm the intended policy profile, and keep a rollback path for removing the SentrySkills block. <br>
Risk: Local logs may retain raw prompts, responses, and task context. <br>
Mitigation: Review log paths before use, avoid supplying secrets unless local retention is acceptable, and define a process for deleting sentry_skill_log data. <br>
Risk: The guard can block or downgrade responses, which may affect normal agent workflows. <br>
Mitigation: Test balanced, strict, and permissive profiles in a controlled workspace before enabling automatic mode for important work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zengbiaojie/sentryskills) <br>
- [Runtime policy profiles](shared/references/policy_profiles.md) <br>
- [Input schema](shared/references/input_schema.json) <br>
- [Guard event schema](shared/references/guard_event.schema.json) <br>
- [Audit record schema](shared/references/audit_record.schema.json) <br>
- [Information trust model](shared/references/trust_model.md) <br>
- [OpenClaw installation guide](install/openclaw_install.md) <br>
- [Codex installation guide](install/codex_install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON event and summary records from local scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces allow, downgrade, or block decisions with trace IDs, event logs, safe-response guidance, and optional redaction.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
