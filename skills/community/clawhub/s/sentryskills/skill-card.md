## Description:

SentrySkills is an automatic security guard for AI agent tasks that provides preflight, runtime, and output checks for prompt injection, data leaks, unsafe commands, and code vulnerabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengbiaojie](https://clawhub.ai/user/zengbiaojie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill package to add local, always-on guard checks around agent tasks that may involve commands, file changes, sensitive data, network calls, or code generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic global setup can give the skill persistent influence over agent behavior.

Mitigation: Review the code before installation and prefer manual or project-scoped configuration unless global activation is explicitly intended.

Risk: Default logging can capture sensitive task content.

Mitigation: Keep generated logs out of source control and avoid using the skill with secrets until logging and path handling concerns are resolved.

Risk: The security evidence flags the release as suspicious.

Mitigation: Pin the exact version or commit, review the configured policy, and deploy only after the identified setup and logging risks are accepted or fixed.

## Reference(s):

- [SentrySkills README](README.md)
- [Installation and Configuration](install/README.md)
- [Input Schema](shared/references/input_schema.json)
- [Guard Event Schema](shared/references/guard_event.schema.json)
- [Policy Profiles](shared/references/policy_profiles.md)
- [Trust Model](shared/references/trust_model.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code, JSON]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and JSON guard results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local guard decisions, trace identifiers, event logs, and redaction or refusal guidance for the agent.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
