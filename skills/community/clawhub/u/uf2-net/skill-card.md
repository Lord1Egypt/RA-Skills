## Description:

Create, manage, and track short URLs using the uf2.net API-first URL shortener for automation and bot workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[setdemos](https://clawhub.ai/user/setdemos)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, list, inspect, and delete uf2.net short links from an agent workflow. It is useful when sharing URLs with custom slugs, checking click counts, or managing public short-link metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a uf2.net API key for authenticated link creation, listing, deletion, and account operations.

Mitigation: Store the API key in a secret store, OS credential manager, or protected session environment variable, and avoid committing it to scripts or shared files.

Risk: Created short links and link metadata are public, and links do not expire unless manually deleted.

Mitigation: Do not shorten sensitive or private URLs, and review each target URL and slug before creating or sharing a link.

Risk: Deleting a link is a remote management action that depends on the supplied link code.

Mitigation: Confirm the link code and associated metadata before deletion.

Risk: The security guidance notes input-escaping weakness for untrusted strings containing quotes or control characters.

Mitigation: Avoid passing untrusted URL, slug, or title values with quotes or control characters until the script uses proper JSON encoding.

## Reference(s):

- [uf2.net API Reference](references/api.md)
- [uf2.net service homepage](https://uf2.net)
- [uf2.net Swagger API docs](https://uf2.net/docs)
- [uf2.net ReDoc API docs](https://uf2.net/redoc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the UF2_API_KEY environment variable for authenticated uf2.net API operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
