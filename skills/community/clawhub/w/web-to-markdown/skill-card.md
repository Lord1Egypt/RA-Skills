## Description: <br>
Converts public web pages to Markdown, extracts image URLs, and batch-downloads page images using online conversion services and local fallback scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josephxie1](https://clawhub.ai/user/josephxie1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and content teams use this skill to convert public web content into readable Markdown, collect image URLs, and download webpage images for review or organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private, authenticated, internal, signed, or token-bearing URLs may be sent to external conversion or scraping services. <br>
Mitigation: Use the skill only with public webpages unless the user has explicitly accepted sending the URL and fetched content to the listed services. <br>
Risk: Downloaded images can be written to local storage, including a default output directory. <br>
Mitigation: Choose the output directory deliberately and review downloaded files before reusing or redistributing them. <br>
Risk: The local fallback scraper requires installing Python dependencies. <br>
Mitigation: Review dependencies before installation and install them only in an appropriate environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/josephxie1/web-to-markdown) <br>
- [markdown.new](https://markdown.new/) <br>
- [defuddle.md](https://defuddle.md/) <br>
- [r.jina.ai](https://r.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, extracted URL lists, and downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write URL lists or downloaded images to user-selected local paths; image downloads default to ~/.openclaw/images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
