## Description: <br>
Plan full trips with real-time FlyAI/Fliggy CLI data, including flights, hotels, attractions, day-by-day itineraries, visa information, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to collect trip parameters, run FlyAI CLI searches, and produce comparison tables with booking links for flights, hotels, attractions, and related travel needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run an unpinned FlyAI/Fliggy CLI. <br>
Mitigation: Manually approve installation, or preinstall a trusted pinned CLI version before using the skill. <br>
Risk: Trip details are sent to the travel provider through CLI calls. <br>
Mitigation: Use the skill only when sharing the requested itinerary, travel dates, and preferences with that provider is acceptable. <br>
Risk: Raw travel requests may be retained in a local .flyai-execution-log.json file. <br>
Mitigation: Delete or disable the local execution log when retained trip details are not needed. <br>


## Reference(s): <br>
- [Trip Advisor ClawHub listing](https://clawhub.ai/xiejinsong/trip-advisor) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands for retries or setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires real-time FlyAI CLI output; every listed travel result must include a booking link.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
