## Description: <br>
Find surfing beaches, diving sites, and underwater adventures, including wave forecasts, dive depth, marine life information, and equipment rental, using flyai real-time travel search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to find bookable surfing, diving, and snorkeling options by running flyai CLI searches and formatting the returned results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an unpinned global flyai CLI installation before it can retrieve travel results. <br>
Mitigation: Install only after reviewing and trusting the flyai npm package, and approve the global CLI installation explicitly. <br>
Risk: The skill can keep hidden local execution logs that may contain raw travel queries. <br>
Mitigation: Avoid sensitive personal travel details unless logging is controlled, and check for or delete .flyai-execution-log.json after use when privacy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/surfing-diving) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with CLI command examples, comparison tables, booking links, and concise fallback messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel data; results must include booking links and should not expose raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
