## Description: <br>
Book flights for yoga retreats and wellness travel destinations, with support for related travel searches such as hotels, train tickets, attractions, itinerary planning, visa information, insurance, and car rental through Fliggy-powered flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to search live flight options for yoga retreats, wellness trips, and related travel needs. The skill guides the agent to collect route parameters, run flyai CLI searches, and present Markdown results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run the external flyai CLI, including a global npm install when the CLI is missing. <br>
Mitigation: Install only in an environment where running flyai travel-search commands and a global npm CLI package is acceptable. <br>
Risk: Flight results and booking links can lead users into workflows involving personal, passport, or payment information. <br>
Mitigation: Treat the skill as a travel-search helper and review booking links before entering sensitive information. <br>


## Reference(s): <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; every flight result should include a booking link.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
