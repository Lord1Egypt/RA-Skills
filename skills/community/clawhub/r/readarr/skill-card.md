## Description:

Interact with Readarr via its REST API to search books, monitor authors, check missing items, trigger downloads, and manage the book library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minerva-care](https://clawhub.ai/user/minerva-care)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to control a Readarr ebook or audiobook manager through REST API calls, including library search, author monitoring, wanted-item review, download triggering, and queue checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Readarr API key to control a user's media library.

Mitigation: Store the API key with restricted file permissions or another safer secret-entry method, and avoid printing it in command output.

Risk: Some documented API actions can remove books, remove queue items, rescan folders, or search all missing books.

Mitigation: Confirm intent before delete, queue removal, rescan, or all-missing-search operations.

Risk: The Docker setup references the linuxserver/readarr develop image tag.

Mitigation: Review or pin the Docker image to a specific version or digest before production use.

## Reference(s):

- [Readarr API Reference](references/api.md)
- [Readarr Setup](references/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include REST API request examples that require a Readarr URL and API key.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
