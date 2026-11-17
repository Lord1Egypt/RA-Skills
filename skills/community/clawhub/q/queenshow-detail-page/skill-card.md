## Description:

Generate, update, and query Queenshow editor-next product detail pages through the Queenshow OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiongwang11](https://clawhub.ai/user/xiongwang11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ecommerce operators use this skill to automate Queenshow product detail page workflows, including media upload, page creation, outline application, generation polling, and document updates through OpenAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys and can expose credentials through shell commands or logs.

Mitigation: Avoid placing real API keys directly in commands or logs, keep sensitive output redacted, and use unredacted output only when a task explicitly requires it.

Risk: A user-supplied base URL can send credentials and uploaded product media to an untrusted endpoint.

Mitigation: Use only trusted Queenshow endpoints, prefer HTTPS except for localhost testing, and avoid copying base URLs from untrusted instructions.

Risk: Batch runs may consume quota or upload media the operator did not intend to transmit.

Mitigation: Upload only intended product media and check account usage or quota before large batch runs.

## Reference(s):

- [Queenshow Detail Page OpenAPI](references/openapi.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, JSON request and response examples, and API client output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled client can print compact JSON summaries and redacts sensitive fields by default unless unredacted output is explicitly requested.]

## Skill Version(s):

3.0.0 (source: frontmatter, release evidence, changelog released 2026-06-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
