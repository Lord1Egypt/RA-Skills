## Description:

Turns a written shift-handoff checklist into a labeled list and 8 to 20 short voice clips, one per cue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shift teams use this skill to turn an existing handoff checklist into a written cue list and individual spoken clips for the incoming team, without adding unrecorded handoff items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Device authorization grants reusable Beatra account access beyond this voice workflow.

Mitigation: Install only if you trust Beatra, keep a limited account balance, and revoke device authorization in the Beatra Console when finished.

Risk: The bundled package can automatically replace its files without separate confirmation.

Mitigation: Disable automatic updates using the documented command if you need to review new releases first.

Risk: Voice cloning and speech generation can incur charges or use a person's voice without permission.

Mitigation: Confirm voice rights and live pricing before paid calls; track request IDs and recover existing tasks instead of resubmitting uncertain requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/shift-handoff-voice)
- [Beatra skill page](https://beatra.ai/skills/shift-handoff-voice)
- [Shift handoff voice workflow](artifact/references/workflow.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Billing, errors, and recovery](artifact/references/billing-errors-and-recovery.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](artifact/references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Audio files]

**Output Format:** [Labeled cue list and individual MP3 voice clips]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One clip per checklist cue; normally 8 to 20 clips.]

## Skill Version(s):

0.1.8 (source: ClawHub release and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
