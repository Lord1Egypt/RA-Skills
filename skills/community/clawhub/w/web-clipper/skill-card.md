## Description: <br>
Save any web page as an Obsidian-compatible Markdown clipping using Jina Reader API for clean content extraction, with support for custom tags, subfolders, and vault paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chatgptnexus](https://clawhub.ai/user/chatgptnexus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users save articles, technical documentation, news pages, and other remote web content as Markdown notes for an Obsidian vault. The skill is useful when a user wants a clean archived copy with source metadata, optional tags, and folder organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send requested URLs and extracted page content to an external reader service. <br>
Mitigation: Avoid using it on private, internal, authenticated, personal, or confidential pages unless the third-party data flow is acceptable. <br>
Risk: The trigger is broad enough that a clipping request may be interpreted from casual save or clip language. <br>
Mitigation: Review the URL before execution and confirm that the page is intended to be clipped. <br>
Risk: The skill may use a Jina API key from the local OpenClaw environment for higher rate limits. <br>
Mitigation: Store only the intended JINA_API_KEY value and rotate it if the local environment or saved output path is exposed. <br>


## Reference(s): <br>
- [Jina Reader API](https://r.jina.ai/) <br>
- [Jina API key](https://jina.ai/?sui=apikey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown file with YAML frontmatter and a short saved-path confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated Markdown clippings to a configured Obsidian vault or the default OpenClaw cache folder.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
