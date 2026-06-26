## Description: <br>
Saves WeChat public account articles as clean Markdown notes in an Obsidian vault, supporting single or batch mp.weixin.qq.com links, natural-language path overrides, and direct writes inside the configured vault root. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amortalsodyssey](https://clawhub.ai/user/amortalsodyssey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch WeChat public account article links, convert the articles into clean Markdown, and save the resulting notes inside a configured Obsidian vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The saver creates folders and may overwrite an existing Markdown note with the same article title. <br>
Mitigation: Set vault_disk_root carefully, test with a non-sensitive folder first, and review the resolved save path before routine use. <br>
Risk: The skill writes local files into the configured Obsidian vault. <br>
Mitigation: Install only when this file-writing behavior is desired and keep vault_disk_root scoped to the intended vault. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amortalsodyssey/wechat-article-to-obsidian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes with YAML frontmatter, plus JSON metadata from parser and saver commands when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The saved note is written under the configured Obsidian vault root, with article images preserved as remote WeChat CDN links.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
