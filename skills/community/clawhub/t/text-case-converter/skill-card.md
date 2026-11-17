## Description:

Convert text in a file to upper, lower, or title case when the user wants to change the capitalization of text in a file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinwangmok](https://clawhub.ai/user/jinwangmok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill to standardize or change capitalization in local text files by printing upper, lower, or title case output without modifying the source file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill prints the provided file's contents to the terminal, which can expose sensitive text through terminal output.

Mitigation: Use it only with files whose contents are acceptable to display, or redirect output according to local data handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinwangmok/skills/text-case-converter)
- [User manual](artifact/MANUAL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text output with file, case, converted content, and status lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads the user-provided local file and prints converted contents; does not modify the source file.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
