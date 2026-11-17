## Description:

Build reliable tool context from command output using artifacts and compact reproducible code queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmaciel](https://clawhub.ai/user/zmaciel)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill when model-facing CLI output needs to be captured once, queried reproducibly, and summarized compactly for model decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the third-party sift-gateway CLI package.

Mitigation: Review the upstream package before installation and pin a known-good version for controlled environments.

Risk: Captured command output may contain sensitive or unrelated private data.

Mitigation: Avoid sending secrets through the gateway unless intended, keep only artifact identifiers and short summaries in model context, and use focused code queries for details.

Risk: Paginated or schema-ambiguous command output can lead to incomplete or misleading model conclusions.

Mitigation: Continue pagination when instructed by response metadata, use the resolved root path or schema metadata, and avoid first-item schema shortcuts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmaciel/skills/reliable-tool-context)
- [OpenClaw integration source](https://github.com/lourencomaciel/sift-gateway/tree/main/docs/openclaw)
- [OpenClaw skill documentation](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize compact summaries, aggregates, or top <= 20 rows rather than full captured payloads.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
