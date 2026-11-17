## Description:

Wiki Js V3 helps agents administer Wiki.js through GraphQL and REST operations for pages, assets, search, tags, trees, history, versioning, and rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyhx1101](https://clawhub.ai/user/nyhx1101)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage Wiki.js content and assets from command-line style workflows, including creating, updating, moving, copying, deleting, searching, restoring, and rendering pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can immediately modify or delete Wiki.js pages, tags, assets, and restored versions.

Mitigation: Review destructive commands before execution and use a least-privilege Wiki.js API token scoped only to the intended wiki and operations.

Risk: A broad production admin token could expose or alter more content than intended.

Mitigation: Avoid broad production admin tokens; rotate tokens if exposed and configure separate tokens for automation.

Risk: Non-local Wiki.js traffic can expose API tokens if WIKIJS_URL is not protected by HTTPS.

Mitigation: Use an HTTPS WIKIJS_URL for any non-local server and avoid sending credentials over plaintext transport.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nyhx1101/skills/wiki-js-v3)
- [Publisher profile](https://clawhub.ai/user/nyhx1101)
- [Wiki.js GraphQL Playground]({WIKIJS_URL}/graphql-playground)
- [Wiki.js REST upload endpoint]({WIKIJS_URL}/u)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WIKIJS_URL and WIKIJS_TOKEN configuration for live Wiki.js API operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
