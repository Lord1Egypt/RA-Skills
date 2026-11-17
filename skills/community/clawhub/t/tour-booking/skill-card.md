## Description:

Sub-agent for outbound listing-office calls to request and confirm property showing slots using a provided call script and structured payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoch](https://clawhub.ai/user/danielfoch)

### License/Terms of Use:


## Use Case:

External real estate workflow operators and agents use this skill to prepare outbound call payloads, place or dry-run listing-office calls, and normalize call results into booking statuses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real outbound calls using provided listing-office phone numbers.

Mitigation: Keep dry-run and human payload review in the workflow before enabling live mode.

Risk: Live requests send client and listing data to the configured ElevenLabs outbound call endpoint.

Mitigation: Use trusted booking inputs, a narrowly scoped ElevenLabs key, and restrict or remove ELEVENLABS_OUTBOUND_URL overrides.

Risk: Output JSON files may contain unredacted call records, client names, addresses, phone numbers, and API responses.

Mitigation: Treat generated output files as sensitive records and redact, retain, or delete them according to the deployment's data-handling policy.

## Reference(s):

- [Tour Booking ClawHub Skill Page](https://clawhub.ai/danielfoch/skills/tour-booking)
- [Call Script Template](references/call-script-template.md)
- [ElevenLabs Environment Variables](references/elevenlabs-env.md)
- [ElevenLabs outbound call API endpoint](https://api.elevenlabs.io/v1/convai/phone-calls)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prepared call payloads, outbound call result records, and normalized booking outcome JSON.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
