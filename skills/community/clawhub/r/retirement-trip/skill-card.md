## Description: <br>
Book flights for retirement celebration trips, with support for related travel planning tasks powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers or agents use this skill to collect route and date details, run the flyai CLI, and present retirement-trip flight options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and execute a global third-party flyai CLI and send travel details to that service. <br>
Mitigation: Pre-install a reviewed, pinned CLI version when possible and require explicit approval before any global npm install or live travel search. <br>
Risk: The skill may activate for broad trip-planning requests and return live booking options. <br>
Mitigation: Confirm route, dates, and traveler intent before execution, and verify every recommendation includes a Book link from detailUrl. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/retirement-trip) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, comparison tables, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output; flight options should include Book links from detailUrl.] <br>

## Skill Version(s): <br>
3.2.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
