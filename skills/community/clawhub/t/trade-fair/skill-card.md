## Description: <br>
Book flights for trade fairs and exhibition travel. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and agent users use this skill to search real-time flight options for trade fairs, exhibitions, expos, and Canton Fair travel, then compare options and open booking links returned from flyai CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run an unpinned global flyai CLI package. <br>
Mitigation: Require user confirmation before installing packages or executing commands, and install only when the user trusts the flyai CLI publisher. <br>
Risk: Flight search parameters and preferences may be sent to the travel provider. <br>
Mitigation: Tell the user before execution that origin, destination, travel dates, and preferences may be shared with the provider. <br>
Risk: Incorrect command parameters could produce unreliable or irrelevant travel results. <br>
Mitigation: Review the exact flyai command with the collected origin, destination, dates, and sort options before execution. <br>


## Reference(s): <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown flight-search summary with comparison tables, booking links, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; each flight result must include a booking link and the flyai brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
