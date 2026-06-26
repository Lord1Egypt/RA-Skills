## Description: <br>
Searches for flights with unaccompanied minor service for children traveling alone and formats live booking options from flyai results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to collect route and date details, run flyai flight searches, and present unaccompanied-minor flight options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run a persistent global third-party flyai CLI package. <br>
Mitigation: Install @fly-ai/flyai-cli only with explicit user approval, verify the package source first, and prefer an already trusted local installation. <br>
Risk: Broad travel triggers could activate the skill for tasks beyond unaccompanied-minor flight search. <br>
Mitigation: Confirm the requested travel task and required route parameters before running commands, and keep execution scoped to the relevant flyai search command. <br>
Risk: Flight results depend on live CLI and network responses, so failures or empty responses can lead to incomplete guidance. <br>
Mitigation: Do not fabricate travel results; retry according to the fallback guidance and tell the user when CLI or network output is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liquanyu123/unaccompanied-minor) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown flight-search summary with comparison tables, booking links, and inline shell commands when setup or execution is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output as the source of flight data and should not emit raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
