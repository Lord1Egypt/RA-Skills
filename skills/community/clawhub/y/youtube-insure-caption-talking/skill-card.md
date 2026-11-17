## Description:

Turns public YouTube insurance captions and advisor-written clause lines into separate short talking clips, one per supplied still.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Insurance and wealth advisors use the skill to turn public YouTube caption material and their own approved clause lines into individual talking clips for review and sharing. It requires supplied still images and rights to any likeness or cloned voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared device authorization grants broad Beatra media and account access.

Mitigation: Review Beatra account permissions and revocation options before connecting; use only if comfortable granting this access.

Risk: The bundled client can update its code automatically without separate approval.

Mitigation: Review the package before installation and disable automatic updates with `python3 scripts/mcp_client.py update --auto off` if changes require explicit review.

Risk: Caption lookups, voice cloning, speech, and video generation may charge Beatra credits.

Mitigation: Check live pricing and billing exposure, and confirm each paid stage before submitting it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/youtube-insure-caption-talking)
- [Insurance caption workflow](references/workflow.md)
- [Caption lookup](references/caption-lookup.md)
- [Authorization and account access](references/installation-and-auth.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Billing and recovery](references/billing-errors-and-recovery.md)

## Skill Output:

**Output Type(s):** [Text, Video files]

**Output Format:** [Markdown status and separate talking video clips]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delivers 2–8 separate clips, typically 2–15 seconds each, with task status and net credits charged for paid operations.]

## Skill Version(s):

0.1.8 (source: ClawHub server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
