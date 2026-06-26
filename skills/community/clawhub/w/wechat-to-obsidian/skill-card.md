## Description: <br>
Clips WeChat public-account articles into Obsidian Markdown notes using a real browser, preserving text, image order, and heading hierarchy while downloading article images into an attachments directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dw1161](https://clawhub.ai/user/dw1161) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and Obsidian users use this skill to convert WeChat public-account article links into local Obsidian notes with preserved headings, inline image embeds, and local image attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens WeChat article pages in a browser, runs page-extraction JavaScript, downloads article images, and writes Markdown plus attachments to local storage. <br>
Mitigation: Install and use it only when comfortable with agent-browser, page extraction, image downloads, and local writes; confirm the destination path before files are written. <br>
Risk: Downloaded images and generated notes may include content from the source article that the user did not intend to keep locally. <br>
Mitigation: Review the generated note, attachments directory, saved path, and reported failed downloads after clipping. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dw1161/wechat-to-obsidian) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, Obsidian image embeds, inline shell commands, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Markdown to a user-confirmed local path and downloads article images into a sibling attachments directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
