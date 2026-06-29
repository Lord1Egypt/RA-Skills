## Description: <br>
Converts Markdown articles into designed 3:4 image cards and a compressed text draft for WeChat Official Account and Xiaohongshu image-post publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and publishing teams use this skill to turn an existing Markdown article into a set of polished 1080x1440 PNG cards plus a text draft under 1000 characters for social publishing. It is intended for article-to-card layout and delivery, not original writing, plain text formatting, or video production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload generated article-derived PNG and text files to Feishu cloud storage using a logged-in account without a clear opt-in step. <br>
Mitigation: Use local-only delivery for private or proprietary articles and require explicit confirmation before any lark-cli upload. <br>
Risk: The skill writes local output files and downloads/renders external images and fonts during card production. <br>
Mitigation: Review generated files and downloaded visual assets before publishing, and prefer trusted local assets for sensitive drafts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edwardwason/xhs-crafter) <br>
- [README](README.md) <br>
- [Skill workflow](SKILL.md) <br>
- [Style system](references/style-system.md) <br>
- [Category cookbook](references/category-cookbook.md) <br>
- [Content planning](references/content-planning.md) <br>
- [Image sources](references/image-sources.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown-guided workflow that creates local HTML/CSS, PNG image files, and a compressed plain-text draft] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 1080x1440 PNG card images and a <=1000-character text draft; may download/render external images and fonts and can optionally upload generated files through Feishu cloud drive tooling.] <br>

## Skill Version(s): <br>
7.3.1 (source: server release metadata and changelog, released 2026-06-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
