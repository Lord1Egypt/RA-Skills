## Description:

Host HTML/Markdown pages and share PDF, Word, or PowerPoint docs as ShareOne short links. Use for publishing, passwords/watermarks, comments, downloads, updates, or Git-backed remote sources for ShareOne content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beep879](https://clawhub.ai/user/beep879)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other ShareOne users use the skill to publish or update HTML, Markdown, and text pages; share PDF, Word, and PowerPoint files; and manage access settings, downloads, and comments through ShareOne links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some commands may send a saved ShareOne API key to an unverified website or over an unencrypted connection.

Mitigation: Before using a real API key, require credentials to be restricted to approved HTTPS destinations and reject insecure redirects.

Risk: Publishing, deletion, or a persistent comment watcher may affect content, links, or sessions beyond the intended scope.

Mitigation: Specify which content may be made public, confirm deletion targets, and explicitly select the project, scope, and session for any persistent watcher.

## Reference(s):

- [ShareOne website](https://shareone.vip)
- [ShareOne ClawHub release](https://clawhub.ai/beep879/skills/shareone)

## Skill Output:

**Output Type(s):** [Text, Share links, HTML pages, Markdown pages, Document files]

**Output Format:** [Text results with ShareOne URLs and operation status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can publish or retrieve HTML, Markdown, TXT, PDF, Word, and PowerPoint content.]

## Skill Version(s):

1.11.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
