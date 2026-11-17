## Description:

Test translation quality with built-in dictionaries and comparison tools. Use when evaluating translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluators use this skill to run simple local checks for translation examples, dictionary lookups, comparison prompts, glossary terms, quality checks, and batch translation test commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some commands may not use arguments as documented, which can produce misleading translation test output.

Mitigation: Review command output before relying on it and confirm behavior with representative inputs.

Risk: Dictionary examples are hard-coded and limited.

Mitigation: Treat dictionary results as sample test data rather than authoritative translation coverage.

Risk: Running the script may create a local data directory under ~/.local/share/translator-pro-test/.

Mitigation: Run in an environment where this local path is acceptable, or remove the directory after testing if persistence is not desired.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/translator-pro-test)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local data directory at ~/.local/share/translator-pro-test/ when the bundled script runs.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
