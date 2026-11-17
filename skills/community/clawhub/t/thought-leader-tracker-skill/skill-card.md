## Description:

Thought Leader Tracker automates collection of podcasts, interviews, and videos about configured thought leaders and generates Markdown reports with summaries, key points, and common themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rickytsao-swordedge](https://clawhub.ai/user/rickytsao-swordedge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content analysts use this skill to track selected thought leaders across podcast and video platforms, collect recent results, and produce daily Markdown digests for review. It is useful for monitoring expert activity, creating daily reports, and spotting repeated themes across tracked people.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may contain inaccurate, stale, or unsanitized remote metadata.

Mitigation: Review report content and links before sharing or using them for decisions, and treat generated Markdown as untrusted content.

Risk: Platform coverage is incomplete because YouTube and Spotify collection are placeholder paths unless credentials and implementation are completed.

Mitigation: Configure required API credentials and verify platform results before relying on coverage claims.

Risk: Daily automation can create recurring external queries and report files.

Mitigation: Install the suggested cron entry only when recurring collection is intended and monitor generated output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rickytsao-swordedge/skills/thought-leader-tracker-skill)
- [Publisher Profile](https://clawhub.ai/user/rickytsao-swordedge)
- [Artifact README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with command-line status text and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are written to daily-logs/ and include titles, links, publish dates, summaries, key points, and common theme analysis.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
