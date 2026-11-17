## Description:

Build and maintain Raycast extensions using React, TypeScript, and the Raycast API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xaif](https://clawhub.ai/user/xaif)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement or fix Raycast extensions by choosing the right Raycast UI component, consulting local API references, and producing concise React and TypeScript guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Raycast extension code may handle passwords, clipboard contents, browser data, OAuth tokens, LocalStorage, or Cache values in ways that expose sensitive data.

Mitigation: Review generated code before use, require explicit user consent before accessing sensitive sources, and redact sensitive values before display, storage, clipboard operations, or AI prompts.

Risk: Examples involving selected files, file writes, or trash actions may lead an agent to modify local files without enough confirmation.

Mitigation: Require a user confirmation step for file-modifying behavior and verify target paths before writing, overwriting, deleting, or moving files.

## Reference(s):

- [ClawHub Raycast Skill Page](https://clawhub.ai/xaif/skills/raycast)
- [List Reference](references/api/list.md)
- [Grid Reference](references/api/grid.md)
- [Detail Reference](references/api/detail.md)
- [Form Reference](references/api/form.md)
- [Actions Reference](references/api/actions.md)
- [AI Reference](references/api/ai.md)
- [Browser Extension Reference](references/api/browser-extension.md)
- [Clipboard Reference](references/api/clipboard.md)
- [OAuth Reference](references/api/oauth.md)
- [Storage Reference](references/api/storage.md)
- [Caching Reference](references/api/caching.md)
- [Toast Reference](references/api/toast.md)
- [HUD Reference](references/api/hud.md)
- [Environment Reference](references/api/environment.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript and TSX code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite the specific local Raycast API reference files used.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
