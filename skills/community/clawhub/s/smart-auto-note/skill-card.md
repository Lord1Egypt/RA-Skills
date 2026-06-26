## Description: <br>
Classifies natural-language note requests and appends them to Obsidian Markdown files for work todos, personal todos, work records, and ideas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miaomiao-d](https://clawhub.ai/user/miaomiao-d) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who maintain Obsidian notes use this skill to capture natural-language todos, work records, and ideas, then append each item to the matching Markdown note file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic persistent note writes may capture unintended or misclassified content in a local Obsidian vault. <br>
Mitigation: Test in a disposable vault first, review low-confidence classification prompts, and keep regular backups of the target Markdown files. <br>
Risk: The skill writes to a hard-coded local folder path. <br>
Mitigation: Change the configured base folder to the intended Obsidian vault before enabling the skill. <br>
Risk: Declared background or message permissions may exceed normal note-capture needs. <br>
Mitigation: Remove unused cron and message permissions unless the deployment explicitly needs them. <br>
Risk: The bundled HTML claims offline and no-third-party behavior while loading Mermaid from a CDN. <br>
Mitigation: Remove the HTML artifact from trusted offline workflows or bundle Mermaid locally before relying on offline or no-third-party operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miaomiao-d/smart-auto-note) <br>
- [Publisher profile](https://clawhub.ai/user/miaomiao-d) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Plain-text confirmations and Markdown note entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends entries to local Obsidian vault Markdown files and does not overwrite existing content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
