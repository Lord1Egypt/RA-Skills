## Description:

Captures agent learnings, errors, corrections, feature requests, and recurring task insights in structured markdown logs for later review and promotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record command failures, user corrections, outdated knowledge, missing capabilities, and recurring best practices. The logged entries support later review, promotion into project memory, or extraction into reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages durable workspace memory, which can preserve sensitive or misleading information if logs are not reviewed.

Mitigation: Keep learning logs local and gitignored by default, avoid storing secrets, and use concise redacted summaries instead of raw transcripts or full command output.

Risk: Optional hook workflows can execute setup or reminder scripts in the agent environment.

Mitigation: Enable hooks only after inspecting the actual scripts and trusting the installation source.

Risk: Promoting entries into agent instruction files can make incorrect guidance persist across future sessions.

Mitigation: Require explicit review before promoting learnings into project memory or agent instruction files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chungvic/skills/self-improvement-vic)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates local learning logs; entries should be reviewed and redacted before promotion into agent instruction files.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
