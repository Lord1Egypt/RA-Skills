## Description:

Creates a labeled three-still launch board from store-provided new-item facts and guides production of a matching set of promotional images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Cafe and retail teams use this skill to plan a new-item launch board and create a coordinated set of promotional stills from confirmed store facts, with approval before paid image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Beatra device token grants broad account access, beyond this still-image task.

Mitigation: Review Beatra account access and revocation options before connecting the skill, especially for paid work.

Risk: The package silently installs verified updates by default, changing its code without a separate approval.

Mitigation: Disable automatic updates with `python3 scripts/mcp_client.py update --auto off` if you want to review changes before updating.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/store-new-item-launch)
- [Beatra skill homepage](https://beatra.ai/skills/store-new-item-launch)
- [Store new-item workflow](artifact/references/workflow.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Image artifacts]

**Output Format:** [Labeled launch board and generated promotional stills]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Initial stills and the remaining pack require separate approval for paid generation.]

## Skill Version(s):

0.1.7 (source: server-resolved release and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
