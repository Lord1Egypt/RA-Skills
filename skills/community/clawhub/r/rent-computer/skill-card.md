## Description: <br>
Helps users request a rental computer when their current machine is underpowered or when they need access to a higher-performance computer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyyinfo](https://clawhub.ai/user/cyyinfo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to view rental computer options and submit a rental request after providing shipping and contact details. It is intended for computer rental workflows involving high-performance computers, GPU servers, or AI workload needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects shipping address and phone or WeChat contact details for a rental application. <br>
Mitigation: Require the agent to display the exact personal data, destination endpoint, and rental request before submission, then obtain explicit final confirmation. <br>
Risk: Broad complaints about computer performance can lead into a rental order flow. <br>
Mitigation: Confirm that the user wants to rent a computer before collecting personal details or submitting any request. <br>
Risk: Rental details are retrieved from and submitted to an external service. <br>
Mitigation: Install and use the skill only when the rental provider and the zhiweisoft.com endpoints are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyyinfo/rent-computer) <br>
- [Rental configuration endpoint](https://zhiweisoft.com/api/openclaw/link) <br>
- [Rental application endpoint](https://zhiweisoft.com/api/openclaw/create) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Markdown-style conversational text with JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Displays rental options, collects address and contact information, and submits a rental application to an external service after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
