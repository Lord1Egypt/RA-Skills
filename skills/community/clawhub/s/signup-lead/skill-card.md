## Description: <br>
Create a signup lead in AgenticCreed by submitting contact and personal details via their public HTTP API endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waqas-orcalo](https://clawhub.ai/user/waqas-orcalo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create AgenticCreed signup leads by submitting required contact details and optional profile fields to the configured HTTP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends personal signup lead data, including contact details and optional profile fields, to AgenticCreed. <br>
Mitigation: Confirm permission to process the person's data, avoid optional sensitive fields unless required, and use only an approved destination service. <br>
Risk: The skill depends on an API key stored in the AGENTICCREED_API_KEY environment variable. <br>
Mitigation: Keep the API key out of prompts, logs, and source files, and rotate it according to local credential policy. <br>


## Reference(s): <br>
- [ClawHub Signup Lead listing](https://clawhub.ai/waqas-orcalo/signup-lead) <br>
- [AgenticCreed signup-leads endpoint](https://gateway.agenticcreed.ai/signup-leads) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Configuration] <br>
**Output Format:** [JSON response from the AgenticCreed HTTP API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTICCREED_API_KEY and sends lead contact fields over HTTPS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
