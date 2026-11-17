## Description:

Generate, parse, validate, and convert UUIDs (v1/v3/v4/v5), ULIDs, and NanoIDs without external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create unique identifiers, inspect UUID or ULID metadata, validate identifier formats, and convert UUIDs between common representations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: UUIDv1 values can expose timestamp and node information when shared publicly.

Mitigation: Use UUIDv4, ULID, NanoID, or deterministic UUIDs unless time-based UUIDv1 metadata is specifically required.

Risk: Very large bulk generation requests can consume excessive resources in shared or resource-limited environments.

Mitigation: Keep --count and --size bounded for the operating environment before running bulk generation.

Risk: The skill runs a local Python CLI for identifier operations.

Mitigation: Install and run it only in environments where local script execution is acceptable, and review the skill before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Python 3.9+ CLI output; no external dependencies.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
