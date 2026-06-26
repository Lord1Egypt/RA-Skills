## Description: <br>
Write a coding standards document for a project using the coding styles from the file(s) and/or folder(s) passed as arguments in the prompt, without modifying analyzed source files unless edits are explicitly requested and confirmed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhauga](https://clawhub.ai/user/jhauga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to analyze selected project files and draft a coding standards document that reflects the project's existing style. It can also summarize inconsistencies and, when explicitly approved, prepare standards-related project changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected files or folders, which can expose sensitive project content if the scope is too broad. <br>
Mitigation: Provide exact file paths or narrow folders, and avoid secrets, environment files, private directories, generated output, and dependency folders. <br>
Risk: The skill can create a standards document or propose README, test, or source-file changes when those options are enabled. <br>
Mitigation: Keep the default read-only posture unless changes are intended, and review any proposed diffs before accepting them. <br>
Risk: Optional external style-reference fetching may be inappropriate for restricted projects. <br>
Mitigation: Disable external style fetching for private or restricted work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jhauga/write-coding-standards-from-file) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown standards document, markdown report, or proposed file changes depending on user-selected options.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a fileName input; may also use folderName, instructions, and configuration-style options. Defaults favor read-only analysis and creating a new standards document.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
