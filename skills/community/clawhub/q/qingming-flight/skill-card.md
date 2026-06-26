## Description: <br>
Helps agents collect Qingming travel details, run live flyai/Fliggy flight searches, and return bookable flight options with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-booking agents use this skill to search Qingming Festival and spring-outing flights, compare recommended, cheapest, fastest, or direct options, and present booking links from live CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install an unpinned global npm package automatically. <br>
Mitigation: Review before installing, approve global npm installation explicitly, and prefer installing or verifying @fly-ai/flyai-cli with a pinned trusted version before use. <br>
Risk: Live flight queries may be sent to flyai/Fliggy. <br>
Mitigation: Use the skill only when users are comfortable sending travel search details to the live flight-search provider. <br>
Risk: The skill can activate for ordinary flight-booking requests beyond Qingming-specific searches. <br>
Mitigation: Confirm the user intends to use this flight-booking workflow before running CLI commands for general travel queries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivan97/qingming-flight) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and summaries with inline booking links and supporting shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight results must come from flyai CLI output and include Book links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
