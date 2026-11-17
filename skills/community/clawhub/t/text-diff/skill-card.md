## Description:

Show line-by-line differences between two text files using Python's difflib, with unified, context, and side-by-side comparison modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill to compare two local text files, inspect line-level changes, and produce unified, context, or side-by-side diff output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved diff output can contain sensitive content from the compared files.

Mitigation: Avoid writing diffs with -o/--output when comparing sensitive material, or store and share the generated diff only in approved locations.

Risk: Documentation mentions Word, PDF, and contract-clause analysis behavior that is not supported by the local text diff implementation.

Mitigation: Use the skill only for local text-file comparison unless those document-analysis features are implemented and reviewed.

## Reference(s):

- [ClawHub Text Diff Skill Page](https://clawhub.ai/harrylabsj/skills/text-diff)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text diff output with optional ANSI color and optional saved text file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares local UTF-8 text files and returns exit codes indicating identical files, differences, file errors, or other errors.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
