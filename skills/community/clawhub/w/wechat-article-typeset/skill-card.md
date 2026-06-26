## Description: <br>
Formats Markdown articles with preset WeChat public-account themes, writes copy-ready HTML, and can generate an edit.shiker.tech preview link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiker1996](https://clawhub.ai/user/shiker1996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editorial teams, and developers use this skill to convert Markdown drafts into themed WeChat public-account HTML and a copy-page preview link. It is intended for preset theme rendering, not AI rewriting or custom article redesign. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The copy workflow uploads rendered article HTML to edit.shiker.tech to create a preview link. <br>
Mitigation: Use the upload workflow only for drafts that are acceptable to send to that external service; avoid confidential drafts, secrets, regulated personal data, and internal announcements unless that upload is approved. <br>
Risk: Generated HTML automatically includes a 稿定助手 branded mini-program header/link. <br>
Mitigation: Inspect article.preset.html before publishing and confirm the inserted branding is acceptable for the article and organization. <br>
Risk: Preview links contain long generated identifiers that can be miscopied if manually transcribed. <br>
Mitigation: Use the script output or generated wechat-preview-url.txt as the source of truth for the preview URL. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shiker1996/wechat-article-typeset) <br>
- [Publisher profile](https://clawhub.ai/user/shiker1996) <br>
- [edit.shiker.tech copy API](https://edit.shiker.tech/api/copy) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated HTML, and preview URL text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces article.preset.html and wechat-preview-url.txt when the copy workflow succeeds.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata; artifact frontmatter and package.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
