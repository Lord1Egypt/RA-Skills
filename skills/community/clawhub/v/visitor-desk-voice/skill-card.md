## Description:

Turns a written visitor reception script into a labeled pack of 8 to 20 spoken clips, one per cue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Front-desk teams use their existing reception script to plan and generate separate greeting, check-in, escort, and other visitor-facing voice clips, with an optional authorized staff-voice clone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Beatra grants broader media-generation, wallet-spending, task, artifact, and voice permissions than this voice-pack workflow needs, with a locally stored bearer token.

Mitigation: Review the shared device authorization before installing; keep the local token private and revoke the connection when it is no longer needed.

Risk: Verified package updates install silently by default and may change local code without a separate approval.

Mitigation: Disable automatic updates with the documented update command if each code change requires review.

Risk: Voice cloning and speech generation spend credits; cloning a staff voice without rights can misuse someone's likeness.

Mitigation: Confirm voice rights and the live cost for each stage, then obtain approval before each paid clone or speech stage.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/visitor-desk-voice)
- [Beatra skill homepage](https://beatra.ai/skills/visitor-desk-voice)
- [Visitor desk voice workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)

## Skill Output:

**Output Type(s):** [Text, Audio files]

**Output Format:** [Labeled cue list and MP3 voice clips]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One clip per written cue; typically 8 to 20 clips.]

## Skill Version(s):

0.1.8 (source: server-resolved release and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
