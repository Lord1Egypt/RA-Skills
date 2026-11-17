## Description:

warehouse-meta helps agents generate, review, persist, and optionally write back data-warehouse table and field metadata comments using Hive or MCP-collected schema evidence and an LLM review pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rickitsui](https://clawhub.ai/user/rickitsui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and analytics platform teams use this skill to improve warehouse metadata coverage, add concise field comments, support review workflows, and improve NL2SQL usability for unclear schemas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Warehouse samples, schema metadata, and DML context may be sent to configured LLM endpoints.

Mitigation: Use approved internal or local model endpoints, sanitize prompts, and avoid sending raw sensitive samples to external services.

Risk: Approved outputs can automatically modify Hive COMMENT metadata at scale in pyhive mode.

Mitigation: Disable Hive writeback and automatic approval until a review, rollback, and change-control process is in place.

Risk: Broad warehouse credentials or scan scope can expose more databases and tables than intended.

Mitigation: Run with least-privilege warehouse credentials and restrict scans to approved databases and tables.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rickitsui/skills/warehouse-meta)
- [Architecture Reference](references/architecture.md)
- [Configuration Template](references/config_template.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands, YAML configuration, JSON schema examples, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist generated metadata to SQLite and, in pyhive mode, write approved comments back to Hive.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
