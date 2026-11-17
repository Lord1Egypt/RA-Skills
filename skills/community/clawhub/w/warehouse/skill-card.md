## Description:

Warehouse is a command-line skill for recording, listing, searching, and exporting warehouse-labeled activity entries from local storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this local CLI to record and inspect warehouse-labeled activities such as ingest, query, schema, validation, and pipeline notes. Reviewers should treat it as a local activity logger rather than a real data warehouse or query engine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is described as a data warehouse toolkit but primarily records user-provided command inputs in local plaintext logs.

Mitigation: Install only when local activity logging is intended, and avoid entering credentials, customer data, private prompts, connection strings, proprietary queries, or other sensitive data.

Risk: Retained local data has no documented purge, redaction, retention policy, or reliable configuration override in the security evidence.

Mitigation: Review and manage the contents of ~/.local/share/warehouse before and after use, and apply external retention or deletion controls where required.

## Reference(s):

- [Warehouse on ClawHub](https://clawhub.ai/bytesagain3/skills/warehouse)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [stdout text with optional JSON, CSV, or text exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores command input history under ~/.local/share/warehouse by default.]

## Skill Version(s):

2.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
