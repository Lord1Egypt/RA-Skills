## Description: <br>
Plans solo travel using FlyAI CLI data for destinations, lodging, attractions, bookings, and itinerary guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and agent users use this skill to plan solo trips with real-time flight, hotel, and attraction data from the FlyAI CLI. It supports safety-conscious, city, and adventure-oriented solo travel workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install a global npm CLI package before use. <br>
Mitigation: Approve installation manually only in a trusted or isolated environment and verify the FlyAI CLI before relying on it. <br>
Risk: The skill can persist raw travel queries in `.flyai-execution-log.json` if filesystem writes are available. <br>
Mitigation: Avoid entering passport, payment, or highly sensitive travel details and disable or delete the local execution log if it is created. <br>
Risk: Travel safety and booking decisions may be incomplete or stale if based only on returned booking data. <br>
Mitigation: Verify safety, visa, booking, and local travel decisions through current official and local sources before acting. <br>


## Reference(s): <br>
- [ClawHub Solo Trip release page](https://clawhub.ai/dingtom336-gif/solo-trip) <br>
- [Solo Trip playbooks](references/playbooks.md) <br>
- [Solo Trip output templates](references/templates.md) <br>
- [Solo Trip fallbacks](references/fallbacks.md) <br>
- [Solo Trip runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands when recovery steps are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include real-time booking links when results are available and should not expose raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
