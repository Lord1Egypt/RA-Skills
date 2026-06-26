## Description: <br>
Book flights for volunteer travel and charity programs, with support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel tasks powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, volunteers, and agents use this skill to search and compare travel options for volunteer travel or charity program trips. The skill guides an agent to collect route and date parameters, run FlyAI CLI searches, and return booking-ready Markdown results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and run a global npm CLI without clear user approval or version pinning. <br>
Mitigation: Require explicit user approval before npm installation or shell execution, and prefer a pinned, local, or sandboxed FlyAI CLI setup. <br>
Risk: Travel search details are sent to the FlyAI/Fliggy CLI provider during execution. <br>
Mitigation: Use the skill only when the user trusts the provider and has agreed to share the needed route, date, and travel preference details. <br>


## Reference(s): <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [ClawHub skill page](https://clawhub.ai/liquanyu123/volunteer-travel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Localized to English or Chinese based on user input; each travel result is expected to include a booking link from FlyAI CLI output.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
