## Description: <br>
Finds student-friendly travel options with real-time flyai CLI results, focusing on budget flights, off-peak departures, booking links, and practical money-saving guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and compatible coding agents use this skill to collect trip details, run flyai flight searches, and format student-oriented travel results with booking links. It is intended for real-time travel search workflows where stale or fabricated prices would be unacceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or ask to install an unpinned global flyai CLI package. <br>
Mitigation: Review installation commands before execution, prefer a pinned or user-local install, and avoid sudo-based global installation. <br>
Risk: Travel search details may be shared with flyai/Fliggy during CLI use. <br>
Mitigation: Use the skill only when sharing route, date, and travel preference details with the travel service is acceptable. <br>
Risk: The execution log may retain raw travel queries in `.flyai-execution-log.json`. <br>
Mitigation: Delete, disable, or avoid persisting the log when raw travel queries should not remain on disk. <br>


## Reference(s): <br>
- [Student Flights on ClawHub](https://clawhub.ai/dingtom336-gif/student-flights) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Runbook](references/runbook.md) <br>
- [Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, concise travel guidance, and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output for travel data and should not expose raw JSON to users.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
