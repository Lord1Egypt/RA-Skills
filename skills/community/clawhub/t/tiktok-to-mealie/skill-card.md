## Description:

Extract recipe information from TikTok links, reconstruct a clean recipe, localize it to the user's language when needed, and import it into Mealie.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elyasuuuuu](https://clawhub.ai/user/elyasuuuuu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn TikTok cooking links into structured, localized recipes and import usable results into Mealie. It is best for execution-focused recipe workflows where a Mealie base URL and API token are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write recipes to Mealie from untrusted TikTok content.

Mitigation: Use a limited Mealie API token, validate extracted content against the documented quality threshold, and stop before import when title, ingredients, or steps are too weak.

Risk: TikTok links and cover images may involve redirects or external downloads.

Mitigation: Resolve and validate redirects and image downloads before import, and avoid broad agent permissions for the configured token.

Risk: Incomplete social-video text can produce inaccurate recipes.

Mitigation: Keep uncertainty explicit, avoid fake precision, and ask for one short confirmation when a partial reconstruction is salvageable but ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elyasuuuuu/skills/tiktok-to-mealie)
- [README](README.md)
- [Configuration](references/configuration.md)
- [Failure modes](references/failure-modes.md)
- [Localization](references/localization.md)
- [Mealie API notes](references/mealie-api-notes.md)
- [Output templates](references/output-templates.md)
- [Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Configuration instructions, Guidance]

**Output Format:** [Short Markdown response, usually a final Mealie recipe link or a brief failure reason]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a Mealie recipe and upload a cover image when configured and quality thresholds are met.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
