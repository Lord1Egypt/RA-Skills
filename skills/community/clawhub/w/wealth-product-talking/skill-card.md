## Description:

Turns an advisor-supplied wealth product factsheet and authorized still images into short spoken clips, one clip per still.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Wealth advisors and educators use this skill to plan factsheet-grounded narration and generate separate 2–15-second talking clips from still images they are authorized to use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent shared Beatra device authorization grants broad access across installed Beatra skills.

Mitigation: Authorize only on a trusted device, keep the credential private, and review the shared connection before installing.

Risk: Verified package updates install silently by default, changing local code without a fresh approval.

Mitigation: Disable automatic updates before use where change control is required; review updates before enabling them again.

Risk: Voice cloning, speech, and video generation each consume credits; uncertain retries can duplicate charges.

Mitigation: Confirm current prices and each stage separately; reuse the same request identity with identical arguments when recovering an uncertain result.

Risk: Talking clips about wealth products could misstate terms or use an unauthorized likeness or voice.

Mitigation: Use only supplied factsheet claims and authorized media; obtain explicit consent for cloning and review clips before sharing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/beatra-ai/skills/wealth-product-talking)
- [Beatra skill homepage](https://beatra.ai/skills/wealth-product-talking)
- [Factsheet talking workflow](references/workflow.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Audio clips, Video clips]

**Output Format:** [Markdown slot list and task results with separate audio and video artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separate 2–15-second clips per still; no stitched video. Paid stages require separate approval.]

## Skill Version(s):

0.1.9 (source: server-resolved release and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
