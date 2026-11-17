## Description:

Saves WeChat public account article links as clean Markdown notes in an Obsidian vault, with single and batch save workflows, configurable vault paths, and an optional browser fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amortalsodyssey](https://clawhub.ai/user/amortalsodyssey)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to archive WeChat public account articles into Obsidian as Markdown notes. It supports single article saves, sequential batch saves, and user-selected vault subpaths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetch scripts can request arbitrary URLs instead of enforcing a WeChat-only host policy.

Mitigation: Use only trusted https://mp.weixin.qq.com article links, and prefer a release that enforces a WeChat host allowlist and HTTPS-only redirects in every fetcher.

Risk: The saver creates folders and writes Markdown files under the configured vault root.

Mitigation: Set vault_disk_root to the intended Obsidian vault and review the target path before saving, especially when using natural-language path overrides.

Risk: Browser fallback loads external pages through Playwright when the fast curl path cannot extract article content.

Mitigation: Use browser fallback only for trusted article links and avoid using the skill for unknown or non-WeChat URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amortalsodyssey/skills/wechat-article-to-obsidian)
- [Publisher profile](https://clawhub.ai/user/amortalsodyssey)
- [Obsidian](https://obsidian.md)
- [obsidian-cli](https://github.com/Yakitrak/obsidian-cli)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes with YAML frontmatter, JSON metadata during inspection, and shell command sequences for fetch, parse, and save steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The saved note includes title, author, publish date, saved date, source, and source URL metadata when available.]

## Skill Version(s):

1.1.2 (source: evidence release and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
