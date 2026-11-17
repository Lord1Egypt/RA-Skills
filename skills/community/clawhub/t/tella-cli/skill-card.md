## Description:

Manage Tella via CLI for videos, clips, playlists, webhooks, transcripts, thumbnails, exports, sharing, and visual edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvynx](https://clawhub.ai/user/melvynx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to manage Tella workspace videos, clips, playlists, exports, transcripts, thumbnails, sharing settings, collaborators, and webhooks from an agent-driven CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can execute a mutable remote installer and npm package code.

Mitigation: Preinstall Bun and api2cli from pinned, verified sources before using the skill, and avoid running remote installer commands blindly.

Risk: The CLI can read, edit, share, export, and delete Tella workspace content.

Mitigation: Confirm targets with read/list commands before destructive actions and use credentials scoped to the least privilege available.

Risk: Stored API tokens and webhook signing secrets are sensitive.

Mitigation: Protect local token storage, avoid exposing tokens in logs or transcripts, and rotate credentials if they may have been disclosed.

## Reference(s):

- [Tella API key settings](https://www.tella.tv/settings/api-keys)
- [Bun installer](https://bun.sh/install)
- [ClawHub skill page](https://clawhub.ai/melvynx/skills/tella-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-driven CLI use should prefer --json output for parsing.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
