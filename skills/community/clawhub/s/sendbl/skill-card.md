## Description:

Create sendbl file-exchange links to request files, send a file, check link status, list files in a link, or delete a link when a user wants to share or collect files over a link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonefremov](https://clawhub.ai/user/antonefremov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and assistant users use this skill to create Sendbl links for collecting files from a counterparty, sending a file through a presigned upload flow, checking link status, listing uploaded files, and deleting links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys, owner tokens, upload links, or download links can expose file-transfer access if pasted into shared logs or transcripts.

Mitigation: Treat SENDBL_API_KEY, owner_token values, and generated links as sensitive credentials; keep them out of shared transcripts and revoke or rotate exposed tokens.

Risk: Raw shell examples can be unsafe when user-supplied text is inserted literally into JSON payloads.

Mitigation: Manually JSON-encode user text or use a safer client before executing commands that include names, filenames, purposes, or messages.

Risk: Deleting a Sendbl link removes the link and all uploaded files.

Mitigation: Confirm the intended link and deletion outcome with the user before running the delete request.

## Reference(s):

- [Sendbl](https://sendbl.com)
- [Sendbl account tokens](https://sendbl.com/account/tokens)
- [Sendbl pricing](https://sendbl.com/pricing)
- [Sendbl API base](https://api.sendbl.com/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENDBL_API_KEY; may handle upload URLs, download URLs, owner tokens, upload link IDs, and file IDs.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
