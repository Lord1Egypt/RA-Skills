## Description: <br>
Generates Chinese web novel cover images by analyzing the title, author name, platform, and genre style, then using GPT-Image-2 to create a finished cover with title and byline text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authors, editors, and publishing workflow agents use this skill to create platform-ready Chinese web novel cover art from a book title, author name, target platform, and optional reference image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the book title, author name, prompt details, and any reference image to the configured image API. <br>
Mitigation: Use only the default OpenAI endpoint or a trusted proxy, and avoid submitting confidential manuscripts, private author data, or sensitive reference images unless the API use is approved. <br>
Risk: The skill writes generated cover images and prompt sidecar files into the selected BOOK_DIR. <br>
Mitigation: Choose an output directory where generated images and prompt text are acceptable to store, review, and retain. <br>


## Reference(s): <br>
- [Cover Styles Reference](references/cover-styles.md) <br>
- [Story Cover on ClawHub](https://clawhub.ai/worldwonderer/skills/story-cover) <br>
- [Skill metadata source link](https://github.com/worldwonderer/oh-story-claudecode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands that generate PNG cover files and prompt sidecar text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GPT_IMAGE_API_KEY plus curl, jq, and base64; may use BOOK_DIR, GPT_IMAGE_BASE_URL, GPT_IMAGE_MODEL, GPT_IMAGE_SIZE, UPLOAD_SIZE, and REF_IMAGE.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
