## Description: <br>
Helps agents search and format flight options for team-building trips and company retreats using the flyai/Fliggy CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and travel coordinators use this skill to gather route and date parameters, run flyai searches, and return bookable flight comparisons for team-building trips and company retreats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to install an unpinned global travel CLI when flyai is unavailable. <br>
Mitigation: Require explicit user approval before installation, prefer an isolated or pinned install, and verify the CLI before running searches. <br>
Risk: Travel route and date details may be sent to the flyai/Fliggy provider during searches. <br>
Mitigation: Use the skill only for intended travel-search workflows and avoid sending sensitive trip details unless the user has approved that provider use. <br>


## Reference(s): <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include bookable result links when available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
