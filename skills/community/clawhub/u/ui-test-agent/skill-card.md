## Description:

This skill helps agents perform UI automation testing on web pages by running browser actions, capturing per-step screenshots, recording a test session, and producing replayable scripts plus a standalone HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[94lfj](https://clawhub.ai/user/94lfj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to convert natural-language web UI test goals into browser automation steps, session records, replayable shell or JSON test scripts, and screenshot-backed HTML test reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recorded sessions and generated HTML reports may contain sensitive screenshots, URLs, selectors, typed values, or embedded files.

Mitigation: Run only trusted test sessions in an isolated workspace and review or redact generated reports before sharing them.

Risk: The skill generates replayable shell and batch scripts from recorded browser commands.

Mitigation: Inspect generated .sh and .bat files before execution and avoid running them against production accounts or systems without review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/94lfj/skills/ui-test-agent)
- [Publisher profile](https://clawhub.ai/user/94lfj)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON session and test-case files, replayable shell or batch scripts, and standalone HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can embed screenshots and recorded URLs, selectors, typed values, commands, timestamps, and step status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
