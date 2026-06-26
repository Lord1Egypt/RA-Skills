## Description: <br>
Search for student exchange program flights and study abroad travel, with support for flight booking, hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel planning through Fliggy and FlyAI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search student exchange and study abroad travel options, collect route and date parameters, execute FlyAI travel-search commands, and present bookable results with comparison tables and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install the FlyAI CLI globally. <br>
Mitigation: Review the package before installation, prefer a pinned CLI version, and install it manually in a controlled environment. <br>
Risk: Travel routes, dates, budgets, and related itinerary details may be sent to FlyAI or Fliggy. <br>
Mitigation: Get user consent before external searches and avoid entering sensitive personal itinerary details unless the user accepts the provider's privacy terms. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liquanyu123/student-exchange) <br>
- [Parameter Collection and Output Templates](artifact/references/templates.md) <br>
- [Scenario Playbooks](artifact/references/playbooks.md) <br>
- [Failure Recovery](artifact/references/fallbacks.md) <br>
- [Execution Runbook](artifact/references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, guidance] <br>
**Output Format:** [Markdown with inline shell commands, comparison tables, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight results must come from FlyAI CLI output and include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
