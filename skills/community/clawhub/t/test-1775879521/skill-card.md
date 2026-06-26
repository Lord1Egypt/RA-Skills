## Description: <br>
Helps agents search private-car day tours and related travel services through the flyai CLI, then format results with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to find private cars with drivers for day tours, half-day trips, and multi-day travel requests. The skill guides the agent to collect a query, run flyai CLI searches, and present bookable results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and run an unpinned global npm CLI. <br>
Mitigation: Install only after user or operator approval, prefer a sandboxed or manually reviewed install, and trust the @fly-ai/flyai-cli package before use. <br>
Risk: Travel queries are sent to the provider and results may influence booking decisions. <br>
Mitigation: Review provider output and booking links before taking action, and verify prices, itinerary details, and terms on the booking page. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; every travel result should include a booking link.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
