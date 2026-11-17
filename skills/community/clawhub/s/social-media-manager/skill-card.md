## Description:

Automates AI-assisted social media content creation, platform adaptation, and draft scheduling or publishing through the Postiz API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tryan310](https://clawhub.ai/user/tryan310)

### License/Terms of Use:


## Use Case:

Social media operators, creators, and marketing teams use this skill to plan, generate, adapt, and schedule posts across connected Postiz social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post or schedule content across connected social accounts through Postiz with broad scope.

Mitigation: Use draft-only operation until the exact platforms, accounts, media, caption, and timing are reviewed and explicitly confirmed.

Risk: Postiz API credentials could be exposed if placed directly in visible command lines or shared outputs.

Mitigation: Use a dedicated least-privilege Postiz API key and avoid placing the key directly in visible command lines.

Risk: Generated social content may be inaccurate, unsuitable for a target audience, or sent to the wrong destination.

Mitigation: Review generated content, platform-specific settings, and destination integrations before any live post or scheduled post.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tryan310/skills/social-media-manager)
- [Publisher Profile](https://clawhub.ai/user/tryan310)
- [Postiz Public API](https://api.postiz.com/public/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with captions, prompts, API examples, scheduling guidance, and review links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific post settings and Postiz API request examples.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
