## Description:

Convert short video moments into GIF-friendly snippets for demos, support, product walkthroughs, and social sharing. Use when a team needs lightweight motion previews instead of full video files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, product teams, operations teams, and creators use this skill to plan concise GIF-friendly motion snippets from source videos for documentation, tickets, presentations, tutorials, demos, and social sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source videos may contain sensitive or private content that should not be processed or shared from the agent environment.

Mitigation: Use videos the user is comfortable processing in the agent environment and review the resulting recommendation before publishing or sharing.

Risk: GIF can be the wrong format when the segment is too long, too detailed, or relies on audio.

Mitigation: Review the recommended segment, duration, size strategy, and GIF-versus-MP4 recommendation before export.

## Reference(s):

- [Video GIF Converter Output Template](references/output-template.md)
- [ClawHub Skill Page](https://clawhub.ai/leooooooow/skills/video-gif-converter)
- [Publisher Profile](https://clawhub.ai/user/leooooooow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown plan with input summary, GIF plan, recommendation, and risks or notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a suggested GIF moment, duration recommendation, size and clarity tradeoff, looping suitability, and GIF-versus-MP4 recommendation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
