## Description:

根据用户主题生成文字游戏剧本，内置19种成熟模板（古代家族、偶像养成、末日求生、校园恋爱、修仙等），支持导出Word文档到桌面。

This skill is ready for commercial/non-commercial use.

## Publisher:

[810722796-lgtm](https://clawhub.ai/user/810722796-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, game designers, and agent users use this skill to create structured Chinese text adventure scripts from built-in genre templates or custom settings, then optionally export the generated Markdown script as a Word document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented export workflow can expose user-controlled title or generated content to shell interpolation.

Mitigation: Use a shell-free process API, pass arguments directly, and send document content through standard input or a temporary file without shell expansion.

Risk: The export workflow writes generated files to the Desktop without explicit opt-in.

Mitigation: Ask for confirmation before writing, show the exact output path, and allow the user to choose or approve the destination.

Risk: The Word export depends on python-docx without a pinned environment.

Mitigation: Use a pinned dependency or locked environment for python-docx before deployment.

## Reference(s):

- [Template reference](artifact/references/templates.md)
- [ClawHub skill page](https://clawhub.ai/810722796-lgtm/skills/text-game-generator)
- [Publisher profile](https://clawhub.ai/user/810722796-lgtm)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown text game script with optional Word document export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scripts include background, characters, opening scene, player options, and mobile-oriented structured panels.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
