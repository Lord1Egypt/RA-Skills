## Description:

AI-powered assistant for creating, scheduling, and analyzing social media content with platform-specific optimization and hashtag research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hughtan93-dev](https://clawhub.ai/user/hughtan93-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to draft platform-specific social posts, research hashtag strategies, plan posting calendars, and review engagement-oriented optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide analytics, competitor, audience, or campaign data that they are not authorized to process.

Mitigation: Use only social media metrics, competitor information, and audience data that the user is authorized to process.

Risk: Generated files can overwrite existing files when users supply output paths to helper scripts.

Mitigation: Review output paths before running scripts with file-writing options.

Risk: Generated social content could be mistaken for automatic account posting or account automation.

Mitigation: Treat the skill as a local content-assistance tool and review content manually before publishing through any social platform.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hughtan93-dev/skills/social-media-manager-xiaoxing)
- [Social Media Best Practices](artifact/references/best_practices.md)
- [Platform Guide](artifact/references/platform_guide.md)
- [Platform Guidelines](artifact/references/platform_guidelines.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional plain text or JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts can print generated posts, hashtag bundles, content calendars, and content ideas to stdout or write JSON files when an output path is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
