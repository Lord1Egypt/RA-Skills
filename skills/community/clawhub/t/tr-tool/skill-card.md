## Description:

Translate or delete characters from input streams. Use for character substitution, deletion, and squeezing repeated characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill for simple local character translation in text streams, such as converting lowercase input to uppercase. The evidence notes that documented deletion and squeezing behavior should not be relied on unless the implementation is updated to support it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact documents delete and squeeze examples, but security evidence reports a functionality mismatch for those behaviors.

Mitigation: Use the skill only for basic character substitution until the implementation is updated and revalidated for delete and squeeze support.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/tr-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local standard-input text transformation guidance; no network, credential, persistence, or privileged behavior is evidenced.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
