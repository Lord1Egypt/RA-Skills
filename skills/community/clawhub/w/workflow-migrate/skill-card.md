## Description:

Migrate N8N/Zapier/Make workflows to production-grade Python or Node.js scripts. Given a workflow description or paste, rewrites automation logic with retry, backoff, logging, and self-healing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevdogg102396-afk](https://clawhub.ai/user/kevdogg102396-afk)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to convert N8N, Zapier, or Make workflows into maintainable Python or Node.js scripts with retries, logging, dry-run support, environment configuration, and operational failure handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Person-specific defaults and the fixed Telegram chat ID could send workflow failure details to an unintended recipient.

Mitigation: Remove person-specific instructions and require users to configure their own opt-in alert destination before using generated workflow alerts.

Risk: Generated workflow scripts may log payloads or dry-run request bodies that contain business data, customer data, or secrets.

Mitigation: Redact payload logging or disable it for sensitive workflows, and review generated scripts before running them against production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevdogg102396-afk/skills/workflow-migrate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated Python or Node.js files, environment examples, dependency manifests, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create workflow scripts, .env.example files, requirements.txt or package.json files, README files, and optional reusable SKILL.md files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
