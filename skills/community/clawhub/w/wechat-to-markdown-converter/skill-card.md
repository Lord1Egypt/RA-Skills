## Description: <br>
Converts public WeChat Official Account article pages into clean Markdown with article metadata, preserved rich text, code blocks, tables, links, and optional local image downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benzking](https://clawhub.ai/user/benzking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, researchers, and archivists use this skill to convert public mp.weixin.qq.com articles into Markdown for review, documentation, migration, or personal archiving workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches remote article pages and may download remote images. <br>
Mitigation: Use trusted WeChat URLs and run conversions in a sandbox when processing untrusted or high-volume inputs. <br>
Risk: The converter writes Markdown and image files to a local output directory. <br>
Mitigation: Choose a dedicated output directory for each conversion to reduce accidental overwrite or file-mixing risk. <br>
Risk: Captcha, restricted pages, or image-only code blocks can produce incomplete output. <br>
Mitigation: Review converted Markdown before relying on it, especially for code-heavy or access-restricted articles. <br>


## Reference(s): <br>
- [WeChat DOM Reference](references/wechat-dom-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with optional YAML frontmatter, local image assets, Python return objects, and concise agent guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single or batch URL conversion, optional image downloading, optional frontmatter omission, and an in-process Python API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
