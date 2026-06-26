## Description: <br>
Save web articles from multiple sources to Obsidian with generated summaries, tags, local image copies, duplicate detection, and optional user notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlalamoon](https://clawhub.ai/user/vlalamoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to archive public web articles into an Obsidian vault as Markdown notes with summaries, tags, source metadata, localized images, and optional personal notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied URLs may be fetched through a third-party reader service. <br>
Mitigation: Use only public URLs that are acceptable to send to that service; avoid private, internal, authenticated, or sensitive links. <br>
Risk: The skill uses anti-scraping fetch methods without clear upfront user controls. <br>
Mitigation: Review target-site permissions and user intent before use, and add an explicit opt-in if stricter controls are required. <br>
Risk: Fetched content and media are written into configured local Obsidian and attachment paths. <br>
Mitigation: Confirm destination paths before running and review downloaded files, especially media size and source. <br>


## Reference(s): <br>
- [Save To Obsidian Publish on ClawHub](https://clawhub.ai/vlalamoon/save-to-obsidian-publish) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter, local image assets, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured Obsidian article and attachment directories; records saved URLs to skip duplicates.] <br>

## Skill Version(s): <br>
2.1.0 (source: evidence.json release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
