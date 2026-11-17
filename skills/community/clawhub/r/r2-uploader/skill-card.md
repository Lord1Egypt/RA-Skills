## Description:

Uses the Wrangler CLI to upload files, remote URL content, and batches of files to Cloudflare R2 object storage and return public access URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redisread](https://clawhub.ai/user/redisread)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare Wrangler commands for uploading local files, remote URL content, or file batches to Cloudflare R2 and to return the resulting object URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish local files or URL-fetched content to Cloudflare R2 through the user's Wrangler login.

Mitigation: Before uploading, confirm the exact local path or source URL, destination bucket and object path, and whether the object will be public; avoid home-directory searches, broad globs, and URL imports from untrusted sources.

Risk: The security guidance identifies the concurrent xargs upload example as unsafe as written.

Mitigation: Do not use the concurrent xargs example without review; prefer tightly scoped sequential uploads or a reviewed parallel command.

## Reference(s):

- [ClawHub r2-uploader skill page](https://clawhub.ai/redisread/skills/r2-uploader)
- [Advanced usage](references/advanced.md)
- [Error handling guide](references/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns upload commands and resulting Cloudflare R2 URLs when available.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
