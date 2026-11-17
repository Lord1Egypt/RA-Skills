## Description:

Scenario-focused Sparki skill for TikTok-native pacing and viral-style edits using Sparki setup, API-key, and upload workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social teams, and developers use this skill to turn local short-form footage into hook-driven TikTok-style edits through Sparki prompts, upload guidance, and CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local videos, prompts, asset IDs, and project metadata are sent to Sparki.

Mitigation: Install only if that transfer is acceptable for the content being edited, and avoid using sensitive media unless the service is approved for it.

Risk: API keys may be stored in local configuration.

Mitigation: Prefer `SPARKI_API_KEY` over saving an API key in the config file, and protect any local Sparki configuration files.

Risk: A custom API base URL can direct uploads and prompts to another endpoint.

Mitigation: Avoid `--base-url` unless the endpoint is fully trusted.

Risk: Downloaded edit results are remote content from the service.

Mitigation: Review downloaded results before reuse or distribution.

## Reference(s):

- [TikTok Viral Editor on ClawHub](https://clawhub.ai/fischerlam/skills/tiktok-viral-editor)
- [Sparki](https://sparki.io)
- [Sparki Telegram upload](https://t.me/Sparki_AI_bot/upload)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides Sparki CLI use for prompt-driven TikTok-style video editing and upload workflows.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter, _meta.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
