## Description: <br>
Build and maintain a local Markdown-based knowledge wiki with Obsidian-style double-links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexfly123lee-creator](https://clawhub.ai/user/alexfly123lee-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to turn raw research materials into a local Markdown wiki with source summaries, concept pages, entity pages, comparison pages, and Obsidian-style links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may perform broad repository writes and git commits that could include unrelated local changes. <br>
Mitigation: Use it in a dedicated repository or review git status, the exact changed files, and the commit message before staging or committing. <br>
Risk: Generated wiki content can introduce incorrect summaries, stale claims, or misleading links. <br>
Mitigation: Review generated pages and lint reports against source materials before relying on or publishing the wiki. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with YAML frontmatter, wiki links, lint reports, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update wiki files and proposes git add/commit commands; review changes before staging or committing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
