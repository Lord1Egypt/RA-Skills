## Description:

Guides coding agents in converting .pptx presentations to web pages, checking fonts, batch processing decks, and embedding or controlling playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spitmaster](https://clawhub.ai/user/spitmaster)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers using AI coding assistants can turn PowerPoint decks into browser-ready HTML, check font issues, batch convert files, and embed or control playback in a website or app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented HTTP example serves converted presentations through URLs without authentication, which may expose decks.

Mitigation: Review the HTTP example before use with sensitive presentations and add authentication and access controls before deployment.

Risk: The batch conversion script was only partially inspected, leaving its security review incomplete.

Mitigation: Review the batch script before running it, especially when processing sensitive presentation files.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/spitmaster/unppt-skill)
- [ClawHub release](https://clawhub.ai/spitmaster/skills/unppt-skill)
- [unppt project](https://github.com/spitmaster/unppt)
- [unppt npm package](https://www.npmjs.com/package/@unppt/unppt)
- [CLI reference](artifact/references/cli.md)
- [JavaScript API reference](artifact/references/api.md)
- [Embedding and playback control reference](artifact/references/embedding.md)

## Skill Output:

**Output Type(s):** [HTML files, Shell commands, JavaScript code, Guidance]

**Output Format:** [Markdown guidance with shell and JavaScript examples; converted HTML or deck JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depending on the selected output, may include media, page, image, and font assets.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
