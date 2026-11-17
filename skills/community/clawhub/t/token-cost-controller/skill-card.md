## Description:

Token省钱管家 helps OpenClaw users reduce token spending with intelligent caching, dynamic model routing, cost reporting, anomaly alerts, and budget controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to monitor token costs, review high-cost skills, route tasks to lower-cost models where appropriate, reuse cached results, and enforce budget controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local cache, cost history, alerts, and control settings can persist sensitive prompts, outputs, or workflow details.

Mitigation: Avoid caching sensitive prompts or outputs unless the storage location and file permissions are acceptable for the deployment environment.

Risk: Disabled-skill and budget controls can block workflows when the host honors those controls.

Mitigation: Review control settings before deployment and keep an operator path for restoring disabled skills or adjusting budget limits.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-oriented text with JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON data for cache, cost history, alerts, and control settings.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
