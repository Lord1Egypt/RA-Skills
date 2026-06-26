## Description: <br>
Show line-by-line differences between two text files using Python's difflib, with unified, context, and side-by-side comparison modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Text Diff to compare two local text files, inspect line-level changes, and optionally save unified, context, or side-by-side diff output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation includes a scenario suggesting Word/PDF parsing and contract-specific semantic analysis, but the implementation reads UTF-8 text files with Python difflib. <br>
Mitigation: Use plain text inputs or convert documents to text before comparison; review contract changes manually when semantic interpretation is required. <br>
Risk: Saving diff output to a chosen local path can replace an existing file if the path is reused. <br>
Mitigation: Choose a new output path or review the destination before using the output-file option. <br>


## Reference(s): <br>
- [ClawHub Text Diff release page](https://clawhub.ai/harrylabsj/text-diff) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or ANSI-colored diff output, including unified, context, or side-by-side layouts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write diff output to a local file and returns exit codes for identical files, changed files, file errors, and other errors.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter and _meta list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
