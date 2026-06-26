## Description: <br>
Syncs WeRead shelf state, reading progress, selected visible book content, and note-ready Markdown into a local workspace using the user's logged-in Chrome session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingchaoxu](https://clawhub.ai/user/mingchaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to sync their own WeRead shelf and selected books into local JSON and Obsidian-ready Markdown so downstream agents can summarize, annotate, or continue note workflows from local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the user's logged-in WeRead browser session. <br>
Mitigation: Run it only on a controlled machine, keep Chrome remote debugging disabled when not syncing, and prefer explicit one-book sync commands. <br>
Risk: Generated reading data and Markdown may contain private reading activity or book content. <br>
Mitigation: Treat output files as private, keep them local by default, and review generated files before sharing or publishing them. <br>
Risk: Publishing can create or overwrite Obsidian notes. <br>
Mitigation: Review generated Markdown before publishing, pass an explicit vault when needed, and confirm overwrite behavior is acceptable. <br>


## Reference(s): <br>
- [Data Contract](references/data-contract.md) <br>
- [Security Policy](SECURITY.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mingchaoxu/weread-assitant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes and JSON files with command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local files under output/weread and output/obsidian; publishing can create or overwrite Obsidian notes through obsidian-cli.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
