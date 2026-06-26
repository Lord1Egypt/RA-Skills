## Description: <br>
Send SMS through the Verimor API, check balance, retrieve delivery reports, list sender headers, and manage blacklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirzakarahan-verimor](https://clawhub.ai/user/mirzakarahan-verimor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Verimor SMS API calls for sending individual or bulk SMS messages, checking account balance, retrieving campaign status, listing sender headers, canceling scheduled campaigns, and managing blacklist entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send paid SMS messages, including bulk, commercial, or scheduled campaigns. <br>
Mitigation: Use restricted or dedicated Verimor credentials and require manual confirmation before every send, especially for bulk recipients, commercial messages, or scheduled campaigns. <br>
Risk: The skill can change campaign or blacklist state, including canceling scheduled campaigns and adding phone numbers to blacklists. <br>
Mitigation: Require explicit confirmation of the campaign ID or phone number before cancellation or blacklist changes, then review the API response with the user. <br>


## Reference(s): <br>
- [Verimor SMS API base endpoint](https://sms.verimor.com.tr/v2) <br>
- [ClawHub skill page](https://clawhub.ai/mirzakarahan-verimor/verimor-sms) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration guidance, Text] <br>
**Output Format:** [Markdown with shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, VERIMOR_USERNAME, VERIMOR_PASSWORD, and VERIMOR_SOURCE.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
