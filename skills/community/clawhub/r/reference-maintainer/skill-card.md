## Description:

Reference Maintainer generates living system reference documentation from source and configuration files so agents can maintain current schema, parameter, architecture, and workflow context across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brad-sl](https://clawhub.ai/user/brad-sl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate and refresh system reference materials from code, schemas, and configuration files. It is intended to reduce stale or missing implementation context when agents resume work across compactions or sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reference files may persist unredacted credentials, tokens, keys, or production connection details copied from source and configuration files.

Mitigation: Run the skill only on scoped, reviewed inputs; redact sensitive values before generation and keep generated references out of version control unless they have been reviewed.

Risk: Generated documentation may be incomplete or stale if extraction misses important behavior or the source changes after generation.

Mitigation: Review generated Markdown, YAML, and JSON against the current source before relying on it as agent context, and regenerate references when source or configuration files change.

## Reference(s):

- [Documentation Template](artifact/references/templates/documentation_template.md)
- [Reference Schema Template](artifact/references/templates/schema.yaml)
- [Reference Maintainer on ClawHub](https://clawhub.ai/brad-sl/skills/reference-maintainer)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown, YAML, and JSON reference files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated references may include extracted source and configuration details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
