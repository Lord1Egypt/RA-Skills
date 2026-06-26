## Description: <br>
Saves WeChat public-account articles as Markdown notes with optional summaries and configurable destinations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlalamoon](https://clawhub.ai/user/vlalamoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to fetch a supplied WeChat article URL and save a Markdown copy into a local folder or configured notes application such as Obsidian or Miaoyan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the article URL supplied by the user. <br>
Mitigation: Avoid internal or sensitive URLs and only run it against article pages intended to be fetched from the local environment. <br>
Risk: The skill writes fetched content into a configured local notes folder. <br>
Mitigation: Set an explicit output directory and review configuration or environment variables before running. <br>
Risk: Notion support is listed in documentation but is not dependable in this version. <br>
Mitigation: Use local, Obsidian, or Miaoyan destinations unless Notion behavior has been separately verified. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vlalamoon/save-article-universal) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown notes with YAML frontmatter, article summary, article body, and source link; CLI output is text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes fetched article content to a configured local destination; Notion support is documented but not reliable in this version.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
