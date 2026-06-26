## Description: <br>
Sub-agent for outbound listing-office calls that builds structured call payloads, can submit live or dry-run ElevenLabs requests, and normalizes booking outcomes into status fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoch](https://clawhub.ai/user/danielfoch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External real estate workflows and agent operators use this skill to prepare, inspect, and optionally place listing-office calls for property showing requests. The skill also helps normalize call results into booking statuses for a parent scheduling workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real outbound calls to listing offices using the prepared destination number and prompt. <br>
Mitigation: Run dry-run first, inspect the phone number and prompt contents, and enable live mode only after confirming the call is authorized. <br>
Risk: Generated payloads and result files may contain client, listing, phone, and scheduling details. <br>
Mitigation: Write outputs only to approved locations and avoid storing or sharing generated files unless the call details are safe to expose. <br>
Risk: Live calls require an ElevenLabs API key and agent ID. <br>
Mitigation: Use a scoped ElevenLabs API key stored in the runtime environment and rotate or revoke it if the workflow no longer needs live calling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/danielfoch/tour-booking) <br>
- [Call Script Template](references/call-script-template.md) <br>
- [ElevenLabs Environment Variables](references/elevenlabs-env.md) <br>
- [ElevenLabs outbound phone calls endpoint](https://api.elevenlabs.io/v1/convai/phone-calls) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON input/output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces outbound-call payload JSON, dry-run or live call result JSON, and normalized booking outcome JSON; live mode requires ElevenLabs credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
