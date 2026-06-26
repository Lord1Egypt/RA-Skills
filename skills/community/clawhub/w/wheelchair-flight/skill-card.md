## Description: <br>
Search for wheelchair accessible flights with mobility assistance options. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and agents use this skill to search for flights that may support wheelchair or mobility-assistance needs, compare recommended, cheapest, fastest, or direct routes, and return bookable options from flyai CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install a global third-party flyai CLI and run external travel searches. <br>
Mitigation: Ask the user to confirm before installing packages or running searches, and review the CLI before deployment. <br>
Risk: Travel details, including accessibility needs, may be sent to an external travel service. <br>
Mitigation: Get user consent before submitting travel details and avoid sending unnecessary sensitive information. <br>
Risk: Search results are not proof that wheelchair assistance is available unless the booking source explicitly confirms it. <br>
Mitigation: Treat returned options as search leads and verify assistance availability with the booking source or airline before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liquanyu123/wheelchair-flight) <br>
- [Publisher profile](https://clawhub.ai/user/liquanyu123) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, accessibility tips, and inline shell commands when setup or execution is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include booking links when flight results are presented.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
