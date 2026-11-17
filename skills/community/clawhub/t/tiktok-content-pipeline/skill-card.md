## Description:

Automates TikTok carousel content creation, smart scheduling, Postiz-based publishing, and analytics-driven optimization for niche accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matttandy855](https://clawhub.ai/user/matttandy855)

### License/Terms of Use:

MIT

## Use Case:

Creators, social media operators, and developers use this skill to generate TikTok carousel assets, manage posting schedules, publish through Postiz, and review performance reports for one or more niche accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing and scheduling actions can affect live TikTok or Postiz-connected social accounts.

Mitigation: Test with a throwaway account first, keep generated posts in draft until reviewed, and avoid cron, --post, and --auto-improve until behavior is confirmed.

Risk: Postiz API keys are sensitive and may be exposed through config files or logs.

Mitigation: Prefer POSTIZ_API_KEY in the environment, use a least-privilege key where possible, keep per-account config files out of version control, and treat logs as sensitive.

Risk: The skill depends on the Postiz CLI and npm packages for publishing, analytics, and image generation.

Mitigation: Pin and review the Postiz CLI and npm dependencies before deployment, and run npm audit after installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/matttandy855/skills/tiktok-content-pipeline)
- [README](README.md)
- [Setup Guide](SETUP.md)
- [Agent Reference](SKILL.md)
- [Postiz](https://postiz.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON configuration, shell commands, generated content files, and analytics reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local account directories, generated media outputs, post metadata, and analytics report files.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
