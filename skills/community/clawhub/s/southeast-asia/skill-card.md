## Description: <br>
Guides agents through Southeast Asia travel planning by using the FlyAI CLI for flight, hotel, attraction, itinerary, visa, insurance, and car-rental searches with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search Southeast Asia flights, lodging, attractions, and related trip services from live FlyAI CLI results. It is intended for booking-oriented Markdown responses that include source booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run an external global FlyAI CLI for travel searches. <br>
Mitigation: Review the CLI package before use, approve installation manually, and restrict execution to environments where global npm installs are acceptable. <br>
Risk: Travel queries may be stored locally in `.flyai-execution-log.json` when file writes are available. <br>
Mitigation: Avoid entering passport or sensitive identity details, and delete or disable the local execution log if travel-query retention is not desired. <br>
Risk: Visa and travel-rule information may be incomplete or stale when CLI data is unavailable. <br>
Mitigation: Verify visa and entry requirements with official government sources before making travel decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/southeast-asia) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when retry guidance is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should be based on FlyAI CLI output, include booking links for listed results, and follow the user's language.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
