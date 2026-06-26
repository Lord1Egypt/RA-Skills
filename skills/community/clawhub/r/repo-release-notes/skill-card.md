## Description: <br>
Draft release notes and changelog entries from a local Git repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aboxhq](https://clawhub.ai/user/aboxhq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to inspect local Git history, compare refs or tags, and turn repository changes into concise release notes or changelog entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Release notes may expose private filenames, internal work details, or security-related changes from repository history and diffs. <br>
Mitigation: Review generated notes before sharing and remove sensitive repository details that are not intended for the audience. <br>
Risk: Generated release summaries can overstate impact when commit messages or diffs are ambiguous. <br>
Mitigation: Compare the draft against the selected Git range and keep only claims supported by commits, diffs, or files. <br>


## Reference(s): <br>
- [Release Note Style](references/release-note-style.md) <br>
- [Repo Release Notes on ClawHub](https://clawhub.ai/aboxhq/repo-release-notes) <br>
- [aboxhq Publisher Profile](https://clawhub.ai/user/aboxhq) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown release note draft with categorized sections and concise assumptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include release range, date, highlights, categorized changes, upgrade notes, and omitted-change assumptions when supported by Git evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
