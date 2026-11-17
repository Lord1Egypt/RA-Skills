## Description:

Guides an agent to create videos from text or reference media using Seedance 2.5, with prompt translation and automatic delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saeedx302](https://clawhub.ai/user/saeedx302)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and other external users use this skill to request text-to-video or reference-guided video generation and receive completed video links or attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The 60-second capability claims conflict with instructions that send 30-second durations and rely on an extension fallback.

Mitigation: Verify achievable duration with the available generation tools before promising a 60-second result; clearly disclose any shorter output or fallback.

Risk: The skill directs automatic generation, reference-media uploads, and retries without confirmation.

Mitigation: Review reference media, expected uploads, and generation costs before enabling unattended use; obtain user approval where appropriate.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/saeedx302/skills/seedance-2-5-60s)

## Skill Output:

**Output Type(s):** [Video files, Text, Links]

**Output Format:** [Video attachments or URLs with a short Markdown delivery note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May translate prompts, upload reference media, retry failed jobs, and track pending generations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
