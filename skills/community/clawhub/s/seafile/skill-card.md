## Description:

Search, download, and upload files in a single Seafile library using a repo token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewreid](https://clawhub.ai/user/andrewreid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with a single token-scoped Seafile library: search filenames or path fragments, download exact file paths, and upload local files into existing library directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can access files in the Seafile library covered by the repo token.

Mitigation: Use the narrowest repo token available and verify the library scope with repo-info before file operations.

Risk: Downloads can save files to the local workspace.

Mitigation: Set an explicit SEAFILE_OUTPUT_DIR and confirm exact remote paths before downloading.

Risk: Uploads may overwrite existing remote files when replace=1 is used.

Mitigation: Prefer replace=0 unless overwriting is intentional, and confirm the target parent_dir before upload.

## Reference(s):

- [Seafile Repo-Token API Notes](references/seafile-api.md)
- [Command Patterns](references/command-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/andrewreid/skills/seafile)
- [Publisher Profile](https://clawhub.ai/user/andrewreid)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and jq with SEAFILE_BASE_URL and SEAFILE_REPO_TOKEN; file operations are limited to the token-scoped Seafile library.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
