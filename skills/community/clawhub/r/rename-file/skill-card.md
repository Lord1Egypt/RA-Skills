## Description: <br>
Rename files in a specified directory by adding a prefix, with prompts for the prefix and directory, a preview, confirmation, and a Node.js execution script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[git-xyz](https://clawhub.ai/user/git-xyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to batch-prefix files in a chosen directory after reviewing a proposed rename preview and confirming the file changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can immediately rename files in the selected directory. <br>
Mitigation: Use it only on test or backed-up folders, confirm the exact directory, and review the preview before approving changes. <br>
Risk: Path-like prefixes may cause renamed files to land outside the intended filename pattern. <br>
Mitigation: Avoid prefixes containing slashes, backslashes, '..', or other path-like text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/git-xyz/rename-file) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and rename summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and can mutate local files after confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
