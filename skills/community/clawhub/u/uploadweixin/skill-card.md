## Description:

Convert Markdown articles into WeChat Official Account friendly inline-style HTML with 12 visual themes, rich-copy preview, macOS rich clipboard support, configurable Upload footer, gallery generation, and validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banlon](https://clawhub.ai/user/banlon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to convert Markdown articles into WeChat Official Account compatible HTML, preview rich-copy output, validate WeChat-safe markup, and optionally generate theme galleries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default Upload / 记忆同步 footer may add branding that a user did not intend to include.

Mitigation: Confirm the desired footer setting before rendering and use --footer disabled or custom footer text when appropriate.

Risk: The inspected artifact references renderer and validation scripts that were not included in the artifact.

Mitigation: Verify the required scripts are available in the installed package before relying on rendering, validation, gallery generation, or clipboard workflows.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/Banlon/agent-skills/tree/main/skills/uploadweixin)
- [ClawHub skill page](https://clawhub.ai/banlon/skills/uploadweixin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and generated HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces article.html and preview.html, with optional theme gallery and macOS rich clipboard outputs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
