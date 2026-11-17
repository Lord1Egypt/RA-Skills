## Description:

AList file management API for OpenClaw that supports upload, download, list, mkdir, rm, mv, search, and offline download workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeshunee](https://clawhub.ai/user/leeshunee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to manage files on an AList cloud-storage server through agent-guided CLI workflows, including listing, uploading, downloading, creating folders, moving, searching, and deleting files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables credential-backed remote file operations on an AList server, including upload, move, and delete actions.

Mitigation: Use a limited AList account where possible and verify target paths before upload, move, or delete operations.

Risk: Broad activation wording could allow destructive file-management commands to be proposed in ambiguous contexts.

Mitigation: Require explicit confirmation before any rm command and review proposed commands before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leeshunee/skills/test-502)
- [AList API specification](references/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AList paths, credentials-related environment variable names, and file-operation command arguments.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
