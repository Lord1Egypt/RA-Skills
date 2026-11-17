## Description:

TikTok App Marketing helps agents automate slideshow marketing for apps or products, including competitor research, AI image generation, text overlays, PosteAhora publishing, analytics tracking, and hook and CTA iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sashadiz](https://clawhub.ai/user/sashadiz)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, growth teams, and app publishers use this skill to set up and operate an agent-assisted TikTok slideshow marketing workflow. The skill guides agents through app profiling, competitor research, image and overlay generation, PosteAhora posting, analytics review, optional RevenueCat conversion tracking, and iterative hook and CTA testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes account-warmup guidance that could be misused to evade platform anti-abuse controls.

Mitigation: Use the guidance only for legitimate account preparation and require review before applying any platform behavior advice.

Risk: API keys and generated marketing data may be stored in local configuration files or reports.

Mitigation: Store secrets in environment variables or a secret manager, keep generated configs and reports out of commits, and review stored social and revenue data before sharing.

Risk: The skill can install packages or set up a persistent analytics cron that processes social and revenue data.

Mitigation: Require explicit approval before package installation or cron setup, and confirm which PosteAhora platforms and RevenueCat data fields are enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sashadiz/skills/tiktok-app-marketing)
- [Server-resolved GitHub import](https://github.com/SashaDiz/skills/tree/main/skills/tiktok-app-marketing)
- [Analytics and Feedback Loop](references/analytics-loop.md)
- [App Category Templates](references/app-categories.md)
- [Slide Structure and Hook Writing](references/slide-structure.md)
- [PosteAhora](https://posteahora.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local marketing profiles, competitor research JSON, generated slideshow assets, post records, analytics reports, and hook-performance tracking files.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
