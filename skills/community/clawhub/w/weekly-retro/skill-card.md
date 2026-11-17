## Description:

Weekly Retro analyzes memory logs to identify accomplishments, recurring patterns, friction points, and forward-looking recommendations for the next week.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other knowledge workers use this skill to turn weekly memory logs into a strategic retrospective with wins, recurring patterns, friction points, unfinished work, recommendations, and a week score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads weekly memory logs and may include sensitive local work details in generated retrospectives.

Mitigation: Review or set the memory directory before running and avoid pointing it at logs that contain information you do not want summarized.

Risk: Persistent vault and history outputs can retain sensitive summaries over time.

Mitigation: Review the output vault path and history path, and delete or relocate generated records according to local retention expectations.

Risk: Default configuration can read SOUL.md and AGENTS.md while analyzing formalized patterns.

Mitigation: Review, disable, or override those paths if workspace instruction files should not be included in analysis.

Risk: The cron example can run the retrospective unattended.

Mitigation: Use scheduled execution only after confirming the configured input, output, and history paths are appropriate.

## Reference(s):

- [Retrospective Format Reference](references/retro-format.md)
- [ClawHub skill page](https://clawhub.ai/newageinvestments25-byte/skills/weekly-retro)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Obsidian-compatible Markdown with YAML frontmatter, plus intermediate structured JSON from the gather and analysis steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local memory, configuration, and optional history inputs to produce persistent retrospective outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
