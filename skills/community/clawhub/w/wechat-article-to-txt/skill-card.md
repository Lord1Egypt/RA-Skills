## Description:

Converts WeChat public account article links into structured personal knowledge-base notes by fetching article content, producing summaries, key points, quotes, tags, and saving Markdown locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afeicn](https://clawhub.ai/user/afeicn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and knowledge workers use this skill to turn WeChat public account articles into Obsidian-ready Markdown notes with summaries, key points, quotes, tags, and related-topic suggestions. It supports saving notes to a configured local vault or writing Markdown files for later import.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires network access, shell execution, and local file-write capability.

Mitigation: Install and run it only in an environment where those permissions are acceptable, and review generated shell commands before execution.

Risk: Article fetching may involve account or session exposure when cookie-based access is used.

Mitigation: Avoid cookie-based fetching unless the user understands the session risk and can limit the account context used for retrieval.

Risk: Weak URL validation and vault path boundaries may allow unexpected network targets or file destinations.

Mitigation: Use explicit WeChat article URLs and an explicit vault path, and avoid untrusted article links until URL validation and vault path containment are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afeicn/skills/wechat-article-to-txt)
- [Publisher profile](https://clawhub.ai/user/afeicn)
- [WeChat article note template](artifact/templates/wechat-article.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown notes, JSON article data, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated notes include YAML frontmatter, summaries, key points, quotes, tags, source links, and optional Obsidian wiki links.]

## Skill Version(s):

1.0.0 (source: server release evidence and _skillhub_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
