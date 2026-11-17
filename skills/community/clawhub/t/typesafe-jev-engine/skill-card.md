## Description:

Use when building typed AI judgments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill as guidance for converting AI decisions into strict JSON/Pydantic contracts, including context classification and task planning schemas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation describes modules that are not all present in the packaged artifact.

Mitigation: Confirm the packaged files before relying on named modules; treat the included Pydantic schema file as the available code reference.

Risk: The skill is Portuguese-oriented and includes a phone-number-like example in the privacy section.

Mitigation: Review examples and terminology before reuse, and sanitize copied content when privacy requirements apply.

## Reference(s):

- [typesafe_schemas.py](references/typesafe_schemas.py)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown with Python/Pydantic and JSON contract examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portuguese-oriented schema guidance; no hidden execution, persistence, credential use, or data exfiltration found in security evidence.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
