## Description:

Test and debug regex patterns against sample text. Use when checking match groups, validating patterns, generating replacements, linting syntax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Regexpal to test regular expressions, inspect matches and capture groups, run replacements, extract matched data from files, and get syntax explanations in a local terminal workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File-based commands can display matching content from user-selected files in the terminal.

Mitigation: Run the skill only on files intentionally selected for inspection and avoid sensitive files unless terminal disclosure is acceptable.

Risk: Untrusted regular expressions or hostile input files can cause long-running regex processing.

Mitigation: Test unfamiliar patterns on small samples first and avoid regexes or files from untrusted sources when reliability matters.

Risk: Untrusted file content can affect terminal output readability or presentation.

Mitigation: Use trusted inputs where possible and review terminal output before acting on highlighted matches or extracted values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/regexpal)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text and Markdown guidance with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces match details, replacement output, extracted groups, or syntax explanations; file-reading commands print selected file content to stdout.]

## Skill Version(s):

3.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
