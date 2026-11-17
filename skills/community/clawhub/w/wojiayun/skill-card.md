## Description:

Provides Wojiayun device management and work-order API access for querying devices, repairs, inspections, maintenance tasks, and multi-project work-order statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mumuxilele](https://clawhub.ai/user/mumuxilele)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to connect agents to Wojiayun APIs for equipment inventory, repair, inspection, maintenance, project switching, work-order creation, file upload, and reporting workflows. Use requires a valid Wojiayun API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe credential handling, including an embedded default API key and local credential files, can expose Wojiayun access.

Mitigation: Use only revocable, least-privilege API keys, rotate any exposed key, remove the embedded default key, and store secrets in a managed secret store.

Risk: Mutable API host configuration can redirect requests or expose business data if the base URL is changed unexpectedly.

Mitigation: Pin the Wojiayun API host, review any base_url changes before use, and run the skill in an isolated environment.

Risk: Work-order creation, file uploads, local exports, and bulk project queries can modify or expose operational data.

Mitigation: Grant only the endpoint permissions required for the task, require operator review for write and upload actions, and limit export locations and retention.

Risk: The production obfuscation build path can perform hidden high-impact local file operations.

Mitigation: Separate build tooling from runtime use, avoid running production build helpers in agent workflows, and review generated files before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mumuxilele/skills/wojiayun)
- [ClawHub publisher profile](https://clawhub.ai/user/mumuxilele)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; runtime calls return JSON-like API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a valid API key and network access to the configured Wojiayun API host.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
