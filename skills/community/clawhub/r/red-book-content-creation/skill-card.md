## Description: <br>
Converts Markdown or plain text into Xiaohongshu-style HTML pages and screenshots, with suggested titles and body summaries for posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenhulove333](https://clawhub.ai/user/wenhulove333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and developers use this skill to turn source material such as articles, technical documents, product notes, or marketing copy into Xiaohongshu-ready visuals and post copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML and PNG files are saved locally. <br>
Mitigation: Run the skill only in workspaces where local generated files are expected and review outputs before sharing. <br>
Risk: Formula rendering may request KaTeX assets from jsDelivr. <br>
Mitigation: Avoid sensitive drafts that should not trigger CDN requests, or review and adjust the generated HTML before rendering. <br>
Risk: Untrusted raw HTML in source content may be carried into generated output. <br>
Mitigation: Use trusted input or sanitize source content before generating and rendering HTML. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenhulove333/red-book-content-creation) <br>
- [KaTeX stylesheet dependency](https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css) <br>
- [KaTeX script dependency](https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with generated HTML, PNG image files, shell commands, and post title/body text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local HTML and PNG files; screenshots target a 680px-wide Xiaohongshu-style layout.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
