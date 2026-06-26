## Description: <br>
Book red-eye flights with late night departure and overnight arrival. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to search red-eye and other travel options through the FlyAI/Fliggy CLI, collect missing trip parameters, and return user-facing flight results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run a third-party travel CLI. <br>
Mitigation: Approve installation and execution manually, and verify the package publisher and version before use. <br>
Risk: Trip details may be sent to FlyAI/Fliggy during searches. <br>
Mitigation: Use the skill only for intended travel searches and avoid entering unrelated or sensitive personal information. <br>
Risk: Flight availability, prices, and booking links depend on external CLI results. <br>
Mitigation: Require current CLI output and valid booking links for every displayed result; do not rely on model memory for travel data. <br>


## Reference(s): <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results must be based on FlyAI CLI output and include booking links when flight options are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
