## Description: <br>
Book flights for shopping trips to outlet malls and duty-free destinations, with related travel booking support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search shopping-trip flights, compare recommended, cheapest, fastest, or direct routes, and receive booking-oriented Markdown results. The skill also guides agents to collect missing travel parameters and recover from CLI failures without fabricating results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt installation and execution of a global third-party CLI. <br>
Mitigation: Require explicit user approval before installation or execution, verify the npm package, and prefer an isolated environment. <br>
Risk: Travel searches may involve sensitive itinerary or personal travel details. <br>
Mitigation: Share only the minimum details needed for the query and use the provider only when the user trusts it. <br>


## Reference(s): <br>
- [shopping-trip ClawHub page](https://clawhub.ai/ivan97/shopping-trip) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results must be based on flyai CLI output and include booking links when flight options are returned.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
