## Description: <br>
Compares live flight prices across multiple travel platforms, identifies low-price dates, and gives informational buy-or-wait guidance for flight purchases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to compare route/date flight prices, scan date ranges for lower fares, and create monitor requests for future price checks. Its buy-or-wait advice is informational and does not replace manual purchase review on the travel provider site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight search details such as cities and dates are sent to the publisher's proxy services. <br>
Mitigation: Install only if this data sharing is acceptable and confirm how PROXY_TOKEN is supplied in the runtime environment. <br>
Risk: Booking links and buy-or-wait recommendations may be incomplete, stale, or unsuitable for a specific purchase decision. <br>
Mitigation: Treat the output as informational and complete any ticket purchase manually on the travel provider site. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/smart-flight-buy) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>
- [Skill homepage](https://rollinggo.store) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance, Shell commands] <br>
**Output Format:** [JSON responses and concise Markdown guidance summarizing flight options, low-price dates, monitor requests, and buy-or-wait advice.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include booking links; monitor mode emits a JSON task for the host agent to schedule.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
