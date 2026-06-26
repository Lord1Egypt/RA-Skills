## Description: <br>
Creates or reuses an Instantly.ai cold email campaign, adds D0/D3/D8 email sequences, and bulk-imports leads through Instantly API v2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales operators, agencies, and developers use this skill to launch cold email outreach campaigns from code, configure schedules and sequences, and upload lead lists without using the Instantly dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Instantly API token and uploads lead contact data to Instantly.ai. <br>
Mitigation: Keep the token in an environment variable, do not commit it in configuration files, and confirm permission and lawful basis before uploading or contacting leads. <br>
Risk: Campaign automation can affect real outreach if campaign settings, email copy, or lead data are incorrect. <br>
Mitigation: Review the campaign configuration and lead file before execution, then test with a small lead file before a full import. <br>
Risk: The Instantly API sequence endpoint may fail, leaving a campaign without the expected email sequence. <br>
Mitigation: Check the script's console warnings after execution and add sequences manually in the Instantly dashboard if the API call fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-instantly-campaign-launcher) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with inline bash, JSON, and JavaScript examples; runtime output is console text from the Node.js script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or reuses an Instantly campaign, attempts to attach email sequences, imports leads, and reports total, imported, skipped, and failed counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
