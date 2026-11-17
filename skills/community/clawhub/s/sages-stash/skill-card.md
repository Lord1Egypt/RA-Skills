## Description:

Returns a non-R18 image URL as a surprise when users search for NSFW content using configured trigger keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ato-z](https://clawhub.ai/user/ato-z)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to respond to NSFW-adjacent image prompts by calling a third-party image API and returning a direct image URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a third-party image API for NSFW-adjacent prompts and may return adult or untrusted image links despite claiming non-R18 output.

Mitigation: Validate that API responses set r18=false, structurally validate returned URLs, and clarify the content policy before treating the skill as low-risk.

Risk: The trigger set is broad and can activate the skill for sexualized prompts in multiple languages.

Mitigation: Narrow the trigger keywords and require deployment review for environments where NSFW-adjacent content is not appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ato-z/skills/sages-stash)
- [Lolicon API endpoint used by the skill](https://api.lolicon.app/setu/v2?num=1&r18=1&size=original)
- [Pixiv image CDN prefix used by the skill](https://i.pixiv.re)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text image URL and Markdown with an inline bash command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a direct Pixiv CDN image URL; the third-party API may have rate limits.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
