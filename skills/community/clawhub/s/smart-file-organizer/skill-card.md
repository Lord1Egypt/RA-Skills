## Description: <br>
File Organizer uses AI semantic analysis of filenames to create Johnny Decimal categories and organize files after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akira82-ai](https://clawhub.ai/user/akira82-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to review a proposed file organization plan, create Johnny Decimal folders, move files into categories, and check for duplicates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move user files and may alter important folders if the wrong source or target path is selected. <br>
Mitigation: Use backed-up or low-risk folders first, provide exact source and target paths, and inspect the proposed move plan before approving changes. <br>
Risk: Duplicate handling can permanently delete files after duplicate detection. <br>
Mitigation: Choose to keep all duplicates unless the files have been separately verified, and review the duplicate report before any delete operation. <br>


## Reference(s): <br>
- [Johnny Decimal Classification Standard](references/johnny_decimal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style interactive prompts, file organization plans, shell commands, and duplicate-check reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create directories, move files, and optionally delete duplicate files after user confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
