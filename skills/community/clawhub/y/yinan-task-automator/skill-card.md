## Description:

Automate repetitive computer tasks including file operations, data processing, web scraping, and API integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinanping-cpu](https://clawhub.ai/user/yinanping-cpu)

### License/Terms of Use:


## Use Case:

Developers and automation users use this skill to create and run file organization, data conversion, API sync, web monitoring, e-commerce, and scheduled workflow automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation configurations can move or write files outside the intended destination when paths or folder rules are unsafe.

Mitigation: Use only trusted configuration files, avoid absolute paths or '..' in folder and output values, review source and destination paths, and run with --dry-run before live execution.

Risk: Recurring jobs can continue running without adequate audit or disable controls.

Mitigation: Create scheduled automations only when there is a documented way to audit, monitor, and disable the job.

Risk: API, web, and e-commerce automations can act on live systems or expose secrets if configured carelessly.

Mitigation: Store credentials outside configs, use environment variables, rate limit external calls, and review configs before running against production systems.

## Reference(s):

- [Task Automator on ClawHub](https://clawhub.ai/yinanping-cpu/skills/yinan-task-automator)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands and JSON, YAML, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task logs and JSON status results when the included runner executes local automations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
