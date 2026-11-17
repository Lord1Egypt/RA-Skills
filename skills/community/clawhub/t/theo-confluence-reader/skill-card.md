## Description:

Converts Confluence requirement pages and their child pages into faithful Markdown exports with metadata and images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcxxtyhd](https://clawhub.ai/user/mcxxtyhd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and analysts use this skill to export Confluence requirement trees into local Markdown files, a collection metadata file, downloaded images, and a ZIP package while preserving source detail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the user to provide Confluence session cookies for private page and image access.

Mitigation: Use a scoped read-only token or protected browser/session integration when possible, and do not paste raw browser cookies into chat.

Risk: The skill can export all reachable Confluence child pages and images from the supplied root page.

Mitigation: Run it only against pages whose full descendant tree may be exported, and review the planned page list before approving long or broad crawls.

Risk: Cleanup and ZIP behavior may affect broader workspace output than expected.

Mitigation: Review and restrict cleanup and packaging steps so they operate only on the current export directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcxxtyhd/skills/theo-confluence-reader)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown files, image files, metadata Markdown, ZIP archive, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates one export directory per run and may package the export as a ZIP archive.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
