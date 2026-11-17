## Description:

Post to social media via VibePost API. Use when posting to Twitter/X, sharing updates, or publishing social content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft and publish social media posts through the VibePost API after confirming the exact text and target platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact embeds a reusable API credential that could enable unauthorized posting outside the skill's consent guardrails.

Mitigation: Revoke the bundled credential and replace it with a per-user secret from an environment variable or secret manager before use.

Risk: Post content is transmitted to the external VibePost service and may publish to public social platforms.

Mitigation: Require a separate confirmation of the exact final post text and platform before every publishing action.

Risk: Local file contents or unintended platform choices could be used to publish sensitive data or reach the wrong audience.

Mitigation: Publish only user-provided approved text and only to the platform explicitly selected by the user.

## Reference(s):

- [VibePost posting API endpoint](https://vibepost-jpaulgrayson.replit.app/api/quack/post)
- [Faberlens safety evaluation](https://faberlens.ai/explore/social-poster)
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/social-poster-hardened)
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts require exact text and platform selection; API responses are returned as formatted JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
