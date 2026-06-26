## Description: <br>
Finds ski resorts and snowboarding destinations, including trail maps, difficulty levels, lift pass prices, equipment rental, snow conditions, and related travel booking support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search for ski and snowboarding destinations, compare resort details, and produce booking-oriented Markdown responses from FlyAI/Fliggy CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install an unpinned global FlyAI CLI before handling a request. <br>
Mitigation: Approve and pin the CLI installation yourself, preferably in an isolated environment. <br>
Risk: Travel queries may be sent to FlyAI/Fliggy services. <br>
Mitigation: Use the skill only when sharing the travel query with FlyAI/Fliggy is acceptable. <br>
Risk: The skill may persist raw user queries in a hidden local execution log. <br>
Mitigation: Ask the agent not to create the log, or delete it after use when queries include personal travel details. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FlyAI CLI output as the data source; successful result responses include booking links.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
