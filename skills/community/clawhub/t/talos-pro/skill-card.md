## Description:

Talos Pro generates multi-platform social media content calendars with daily schedules, A/B caption variants, content angles, repurposing guidance, and export files for scheduling tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to create 8- or 12-week social media calendars for Twitter, LinkedIn, Instagram, Threads, and TikTok. It is intended to help plan posting schedules, draft caption variants, generate content angles, and export calendar files for scheduling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install step uses an unpinned dependency install with --break-system-packages, which can modify the system Python environment.

Mitigation: Install and run the skill in an isolated virtual environment and pin the rich dependency before use.

Risk: The skill writes generated JSON, CSV, and Markdown export files to the current working directory.

Mitigation: Run the skill from a directory intended for generated marketing plans and review exported files before importing them into scheduling tools.

Risk: Generated captions, posting times, and content angles may be generic or unsuitable for a specific brand or platform policy.

Mitigation: Review and edit generated calendars before publication, especially claims, hashtags, timing assumptions, and platform-specific content.

## Reference(s):

- [Talos Pro ClawHub release page](https://clawhub.ai/occupythemilkyway/skills/talos-pro)
- [Talos Pro homepage metadata link](https://clawhub.ai/occupythemilkyway/talos-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown instructions with inline shell and Python code; runtime exports JSON, CSV, and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LICENSE_KEY and BRAND_TOPIC environment variables; optional platform, posting cadence, content pillar, tone, calendar length, and A/B variant settings control generated output.]

## Skill Version(s):

1.0.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
