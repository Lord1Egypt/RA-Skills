## Description: <br>
通用翻译工具(免费版) helps agents translate everyday text and single Markdown files across languages while preserving formatting, technical terms, code blocks, links, and tone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual users and developers use this skill to translate daily text, project documentation, README files, and code comments while preserving Markdown structure and technical identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests shell execution even though its normal translation workflow does not require executable payloads. <br>
Mitigation: Run it with shell execution disabled unless a user explicitly approves a specific command. <br>
Risk: The skill can create or overwrite translated files during single-file translation. <br>
Mitigation: Require user confirmation before writing files and use it only on files intentionally provided for translation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/universal-translate-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown or plain text translation output; optional translated Markdown files with language-code suffixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves Markdown formatting, code blocks, URLs, paths, variable names, CLI commands, and technical terms when translating.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
