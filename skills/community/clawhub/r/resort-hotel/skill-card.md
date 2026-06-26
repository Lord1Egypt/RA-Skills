## Description: <br>
Book flights to resort hotels and all-inclusive vacation destinations. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-booking agents use this skill to search resort-focused flight options and produce booking-oriented Markdown results from flyai CLI output. The skill is aimed at real-time flight discovery, comparison, and booking-link presentation rather than general travel advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install and run an unpinned global flyai CLI package. <br>
Mitigation: Review and install the flyai CLI in an isolated environment, preferably with a pinned version, before enabling the skill. <br>
Risk: Travel-search details may be sent to an external travel CLI service. <br>
Mitigation: Use the skill only when users accept sending route, date, and booking-search details to the external service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/resort-hotel) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
