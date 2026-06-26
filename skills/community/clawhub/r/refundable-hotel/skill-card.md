## Description: <br>
Find hotels with free cancellation policy - book with confidence, change plans without penalty; supports hotel, flight, train, attraction, itinerary, visa, insurance, and car rental workflows powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search for refundable or free-cancellation hotel options and format real-time booking results from the flyai CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install and run a global third-party npm CLI. <br>
Mitigation: Review the CLI package before installation and install it only in environments approved for third-party command-line tools. <br>
Risk: Travel-search details may be sent to flyai or Fliggy when the CLI is used. <br>
Mitigation: Avoid entering sensitive personal or business travel details unless that data sharing is acceptable. <br>
Risk: Local execution logs may store raw travel queries. <br>
Mitigation: Treat logs as potentially sensitive and clear or protect them according to local data-handling policy. <br>
Risk: Refundability and cancellation terms may change or differ from summarized results. <br>
Mitigation: Verify cancellation terms on the booking page before relying on a hotel result as refundable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiejinsong/refundable-hotel) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Hotel results should be based on flyai CLI output and include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
