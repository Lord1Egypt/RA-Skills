## Description:

Generate a patient-controlled SMART Health Link (SHL) QR code for sharing health records with a clinic or provider, covering consent, token retrieval, SHL generation, QR rendering, and private manage-link delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aks129](https://clawhub.ai/user/aks129)

### License/Terms of Use:

MIT-0

## Use Case:

External patients and care teams use this skill to create revocable SMART Health Link QR shares for clinic intake or provider record exchange after confirming record scope, expiry, and label with the patient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive health-record sharing and depends on trusted SHL server and FHIR token tooling.

Mitigation: Install only where the SHL server and FHIR token tools are trusted and configured for the intended patient population.

Risk: A QR code that directly encodes health data would create an unrevocable plaintext copy of protected information.

Mitigation: Encode only the shlink:/ URI returned by shl_generate and stop if a real SHL cannot be generated.

Risk: Sharing the manage link with clinics or group chats would expose revocation and access-log controls.

Mitigation: Deliver the manage link privately to the patient only and label it as private.

Risk: Overbroad scope or long expiry can expose more health information for longer than necessary.

Mitigation: Confirm profile, label, and expiry before generation, and choose the shortest practical expiry.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aks129/skills/share-health-qr)
- [Publisher Profile](https://clawhub.ai/user/aks129)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with structured workflow steps, tool-call examples, shell commands, and user-facing response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces patient-facing instructions and agent workflow guidance for generating SHL QR shares; the QR must encode only the returned shlink:/ URI.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
