## Description: <br>
Plan self-driving road trips, including optimal routes, car rental, scenic stops, fuel stations, recommended rest areas, and related travel booking workflows powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to plan self-driving trips with real-time route, car rental, attraction, hotel, flight, and booking information returned through the flyai CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install and run an unpinned global npm CLI package for travel searches. <br>
Mitigation: Install only when the user trusts the Flyai CLI, and review CLI installation and execution before use. <br>
Risk: The skill can persist raw trip queries in a local .flyai-execution-log.json file. <br>
Mitigation: Avoid entering sensitive personal or payment information, and delete or disable local trip-query logging when privacy is a concern. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/road-trip) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output as the data source; every displayed travel result must include a booking link.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
