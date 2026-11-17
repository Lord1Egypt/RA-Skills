## Description:

Process external code review feedback with technical rigor. Use when receiving feedback from another LLM, human reviewer, or CI tool. Verifies claims before implementing, tracks disposition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to process external code review feedback, verify each item against the current codebase, and apply confirmed fixes with an evidence-backed response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed feedback items may lead the agent to edit repository files and run normal verification commands.

Mitigation: Review the valid-items summary before confirming the launch prompt, and inspect the final implemented/rejected table with file citations.

Risk: Incorrect reviewer feedback could produce unnecessary or harmful code changes if accepted without verification.

Mitigation: The skill requires tool-based verification and evidence for every item before fixes are launched.

## Reference(s):

- [Skill Integration](references/skill-integration.md)
- [Receive Feedback ClawHub Page](https://clawhub.ai/anderskev/skills/receive-feedback)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with tables, file citations, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository edits and verification command results when confirmed fixes are applied.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
