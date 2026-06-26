## Description: <br>
Tianshu Huangdao helps agents answer Chinese almanac, auspicious-date, I Ching, zodiac fortune, and naming requests using traditional calendrical and metaphysical reference data, with some features requiring a 1.68 USD PayPal payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makclaw](https://clawhub.ai/user/makclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users ask an agent for Chinese almanac guidance, auspicious dates, zodiac or I Ching readings, and Chinese naming suggestions. The skill guides the agent through free queries and paid PayPal-gated API calls when a fuller fortune, hexagram, or naming report is requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger paid external service calls for selected features. <br>
Mitigation: Confirm the 1.68 USD PayPal charge with the user before invoking paid features. <br>
Risk: Fortune and naming requests may involve personal details such as birth dates, surnames, or gender. <br>
Mitigation: Send personal details to sinodata.io only when the user intentionally requests the corresponding reading or naming result. <br>


## Reference(s): <br>
- [Tianshu Huangdao ClawHub listing](https://clawhub.ai/makclaw/tianshu-huangdao) <br>
- [Publisher profile](https://clawhub.ai/user/makclaw) <br>
- [sinodata.io API gateway](https://sinodata.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown, Configuration] <br>
**Output Format:** [Markdown and HTTP API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for Traditional Chinese user-facing responses; paid features require confirming the PayPal charge and passing a paypal_order_id.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
