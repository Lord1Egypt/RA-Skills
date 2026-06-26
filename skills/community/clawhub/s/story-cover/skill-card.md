## Description: <br>
Story Cover helps agents generate Chinese web-novel cover prompts, call a GPT image API, and save finished cover images with prompt records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to turn a book title, author name, target platform, and optional reference image into a platform-sized Chinese web novel cover. It guides style selection, prompt construction, GPT image API calls, output saving, and quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Book titles, author names, prompts, and optional reference images may be sent to OpenAI or a configured compatible proxy. <br>
Mitigation: Use a trusted GPT_IMAGE_BASE_URL endpoint, avoid sensitive reference images, and confirm users are comfortable sharing the supplied creative material. <br>
Risk: Generated covers and prompt copies are written under BOOK_DIR, which may expose drafts or reference details if the directory is shared. <br>
Mitigation: Set BOOK_DIR to an appropriate local output directory and review generated files before sharing or uploading. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/worldwonderer/skills/story-cover) <br>
- [Publisher Profile](https://clawhub.ai/user/worldwonderer) <br>
- [Cover Style Reference](references/cover-styles.md) <br>
- [OpenClaw Metadata Source](https://github.com/worldwonderer/oh-story-claudecode) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Images, Files] <br>
**Output Format:** [Markdown guidance with bash commands; generated outputs are PNG image files and prompt/reference text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GPT_IMAGE_API_KEY plus curl, jq, and base64. May send book titles, author names, prompts, and optional reference images to OpenAI or a configured compatible proxy.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
