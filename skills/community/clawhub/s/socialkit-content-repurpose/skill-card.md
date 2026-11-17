## Description:

Turns one source (a video script, blog post, transcript, talk or notes) into separate, platform-appropriate drafts for Facebook, Instagram, Threads and other connected platforms, each in its own post folder ready for approval and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

External users managing social media content can turn a video script, article, transcript, talk, or notes into platform-specific drafts. They review each draft before approving it for a separate publishing step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output folder retains a local copy of the source, which may contain private material.

Mitigation: Choose an output folder appropriate for the source's sensitivity.

Risk: A platform-specific draft could misstate or add claims beyond the source.

Mitigation: Review every draft against the source and approve it before publishing.

Risk: The required socialkit-social-core dependency and any publishing or calendar skills were not supplied for this review.

Mitigation: Review those components separately before approving or publishing drafts.

## Reference(s):

- [Adapting one source for several platforms](references/adapting.md)
- [ClawHub release](https://clawhub.ai/ahmadhussain0335/skills/socialkit-content-repurpose)

## Skill Output:

**Output Type(s):** [Text, JSON files, Guidance]

**Output Format:** [Platform-specific post text in per-platform post.json files, plus a brief summary of how each draft differs from the source.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One post folder per platform; drafts are checked against platform limits.]

## Skill Version(s):

0.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
