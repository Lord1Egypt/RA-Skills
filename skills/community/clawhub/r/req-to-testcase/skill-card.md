## Description:

Generates comprehensive test cases from requirement documents and can export the results as XMind files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deathknightorg](https://clawhub.ai/user/deathknightorg)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, product teams, and developers use this skill to turn uploaded requirement documents or pasted requirements into structured requirement breakdowns, test cases, and XMind mind maps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unpinned dependencies into the system Python environment can affect unrelated tooling or introduce unexpected package changes.

Mitigation: Use an isolated virtual environment with pinned dependencies instead of the documented --break-system-packages commands.

Risk: The skill reads user-uploaded requirement documents and generates downloadable outputs, so it can process the wrong file if the input is ambiguous.

Mitigation: Confirm the exact uploaded document before running the reader or generating XMind output.

## Reference(s):

- [Test coverage strategy reference](references/test-coverage.md)
- [ClawHub skill page](https://clawhub.ai/deathknightorg/skills/req-to-testcase)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown tables and .xmind files, with shell commands when reading documents or exporting XMind.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process uploaded TXT, Markdown, Word, PDF, spreadsheet, and CSV requirement files; XMind export depends on optional Python packages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
