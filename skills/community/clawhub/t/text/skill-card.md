## Description: <br>
Transform, format, and process text with patterns for writing, data cleaning, localization, citations, and copywriting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide common text workflows, including writing, text data cleaning, academic citation handling, marketing copy, and localization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some examples may be run by an agent as shell commands that edit files. <br>
Mitigation: Confirm target files before execution and use version control or backups before in-place edits. <br>
Risk: Examples may inspect .env or configuration files that can contain secrets. <br>
Mitigation: Treat configuration and .env files as sensitive and avoid exposing secret values in prompts, logs, or outputs. <br>
Risk: Text-processing guidance can introduce incorrect or misleading edits if applied without review. <br>
Mitigation: Review proposed transformations, citations, translations, and copy changes before using them in production content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/text) <br>
- [Creative Writing Patterns](writing.md) <br>
- [Text Data Processing](data.md) <br>
- [Academic Text and Citations](academic.md) <br>
- [Marketing Copy and Email](copy.md) <br>
- [Translation and Localization](localization.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline examples, command snippets, regexes, and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose text transformations, citations, copy variants, localization checks, parser choices, and file-processing commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
