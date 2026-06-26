## Description: <br>
Search and compare round-trip flights with return dates, including total cost for both legs and bundled-versus-separate booking comparisons for flight and related Fliggy travel services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to retrieve real-time round-trip flight options, compare bundled and separate-leg pricing, and produce booking-oriented summaries from flyai CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run a global third-party FlyAI CLI for travel searches. <br>
Mitigation: Ask before any npm install, prefer a pinned or manually reviewed CLI setup, and proceed only when the user accepts the third-party dependency. <br>
Risk: Raw travel queries may be persisted locally in .flyai-execution-log.json. <br>
Mitigation: Remove or disable the local execution log when users do not want travel queries retained. <br>
Risk: Booking-critical travel, visa, or payment-related information could be incomplete or unsuitable for final decisions. <br>
Mitigation: Avoid entering passport or payment details through the skill and verify visa or booking-critical information with official sources. <br>


## Reference(s): <br>
- [Parameter and Output Templates](references/templates.md) <br>
- [Return-Flight Playbooks](references/playbooks.md) <br>
- [Fallback Procedures](references/fallbacks.md) <br>
- [Execution Log Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking-link tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; user-facing results should include Book links and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
