## Description:

Test, match, extract, replace, explain, and validate regular expressions from the command line with 25+ named common patterns and zero external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, test, debug, explain, and validate regular expressions, including common named patterns for emails, URLs, IP addresses, phone numbers, dates, UUIDs, and related text formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool can read and print content from any file path explicitly passed with --file.

Mitigation: Run it only on intended files and avoid sensitive paths unless that content is meant to be searched and displayed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/regex-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The findall command can emit structured JSON with match text, offsets, and captured groups; other commands emit terminal text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
