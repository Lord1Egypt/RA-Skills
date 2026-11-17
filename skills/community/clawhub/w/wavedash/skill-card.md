## Description:

Use when building, integrating, testing, uploading, publishing, or preparing a browser game for Wavedash, including CLI setup, Wavedash SDK features, multiplayer, achievements, leaderboards, cloud saves, player identity, user-generated content, store metadata, pricing, and content guidelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavedash](https://clawhub.ai/user/wavedash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game engineers use this skill to build or adapt browser games for Wavedash, integrate SDK features, test builds locally, upload releases, and prepare store metadata for publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup guidance includes remote install scripts and mutable package installs.

Mitigation: Review the installation source before use; prefer a signed or package-manager install with a pinned version and checksum when available.

Risk: Automation can use WAVEDASH_TOKEN for authenticated Wavedash actions.

Mitigation: Keep tokens in a secret manager or local environment only, avoid committing credentials, and use automation output flags that reduce accidental token exposure.

Risk: Publishing a build makes it live for players.

Mitigation: Publish only after explicit user approval, then verify the uploaded build in a fresh browser.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wavedash/skills/wavedash)
- [Wavedash quickstart](https://docs.wavedash.com/getting-started/quickstart)
- [Wavedash CLI commands](https://docs.wavedash.com/cli/commands)
- [Wavedash SDK overview](https://docs.wavedash.com/sdk/overview)
- [Wavedash engine guides](https://docs.wavedash.com/engines)
- [Wavedash publishing guide](https://docs.wavedash.com/publishing/upload)
- [Wavedash content guidelines](https://docs.wavedash.com/publishing/content-guidelines)
- [CLI workflow reference](references/cli.md)
- [SDK integration reference](references/sdk.md)
- [Publishing reference](references/publishing.md)
- [Game quality reference](references/game-quality.md)
- [Engine guides reference](references/engines.md)
- [Wavedash docs map](references/docs-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Wavedash CLI commands, SDK integration snippets, configuration guidance, and publication checklists.]

## Skill Version(s):

0.1.0 (source: evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
