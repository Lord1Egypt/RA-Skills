## Description: <br>
Fetches live theme park wait times and park metadata from Queue-Times.com JSON APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adaclaw](https://clawhub.ai/user/adaclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to resolve theme park IDs and fetch or summarize live Queue-Times.com wait times, ride status, park metadata, and closures for requested parks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent makes outbound requests to Queue-Times.com when users ask for park wait times. <br>
Mitigation: Use the skill only when that external lookup is expected, and avoid sending sensitive personal details in park queries. <br>
Risk: Queue time data is refreshed about every 5 minutes and may not reflect second-by-second conditions. <br>
Mitigation: Describe results as recently refreshed live data, and avoid presenting wait times as instantaneous measurements. <br>
Risk: Queue-Times.com requires prominent attribution when API data is displayed. <br>
Mitigation: Include a visible "Powered by Queue-Times.com" attribution link whenever presenting fetched queue-time data. <br>


## Reference(s): <br>
- [Queue-Times.com API documentation](https://queue-times.com/pages/api) <br>
- [Queue-Times.com](https://queue-times.com/) <br>
- [Reference excerpts](reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/adaclaw/theme-park-queue-times) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text response with Queue-Times.com attribution when API data is presented] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires outbound HTTPS requests to Queue-Times.com; live data refreshes about every 5 minutes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
