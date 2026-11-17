## Description:

Bootstrap the SEO + GEO skill suite by installing the seogeo binary and writing all 48 SEO/GEO skills into detected agent tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this setup skill to install, verify, and update the seogeo binary and the SEO/GEO skill suite across supported agent tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow uses remote installer scripts from the internet.

Mitigation: Install only when the publisher and referenced repository are trusted; prefer a version-pinned or signed installer workflow where available.

Risk: The skill can modify every detected agent tool installation when run with the all target.

Mitigation: Run a dry-run first and choose a single explicit target such as codex unless broad installation is intentional.

Risk: Future updates repeat the remote script execution pattern.

Mitigation: Review update commands and release provenance before applying each update.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-geo-skill)
- [Source repository referenced by the skill](https://github.com/asale-ai/seo-geo-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, verification, dry-run, update, and credential-check commands.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
