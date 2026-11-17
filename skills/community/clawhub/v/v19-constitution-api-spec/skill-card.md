## Description:

Documents the CORE CONSTITUTION MANIFEST API v1.0.2 for external agent access to the V19 cognitive-governance protocol, including the continuous stability evaluator for ETHIC_005/006.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill as an API specification for governance validation, bootstrap status checks, attention balance reporting, audit redundancy lookup, interactive governance queries, self-registration, and conformance testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact publishes a shared public governance API key without clear scope, expiry, or safety limits.

Mitigation: Before using the key, confirm it is sandboxed, low-privilege, rate-limited, and approved for redistribution; prefer self-registration for a scoped key when available.

Risk: The referenced conformance test suite is a separate package and is not part of this artifact.

Mitigation: Review, scan, and pin the conformance-test-suite package before installing or running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyanfeng1234/skills/v19-constitution-api-spec)
- [Publisher profile](https://clawhub.ai/user/liuyanfeng1234)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown API specification with endpoint descriptions, tables, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no executable code is included in the artifact.]

## Skill Version(s):

1.0.2 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
