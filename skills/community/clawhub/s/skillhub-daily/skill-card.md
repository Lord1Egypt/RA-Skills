## Description:

SkillHub Daily scans SkillHub.cn rankings, category searches, and keyword searches to produce daily China-focused skill recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and teams use this skill to discover China-adapted SkillHub skills, active developers, and daily recommendations based on rankings, categories, and local memory keyword matching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local memory keywords and uses them for recommendation matching.

Mitigation: Use it only when local memory keyword processing is acceptable; the release notes and security evidence state that raw memory content is not transmitted and recommendation output records counts instead of keyword values.

Risk: The skill can publish generated reports to Obsidian, IMA, and Feishu when credentials and destinations are configured.

Mitigation: Run with --skip-push unless external uploads are intended, and verify destination paths, knowledge bases, and credentials before enabling publishing.

Risk: The security review notes weak scoping around dependency installation and output paths, including untrusted --date values.

Mitigation: Prefer a pinned local skillhub CLI, keep credentials in local environment variables, and avoid untrusted --date values until path validation is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardwason/skills/skillhub-daily)

## Skill Output:

**Output Type(s):** [markdown, JSON, files, shell commands, guidance]

**Output Format:** [Markdown briefings, JSON recommendation files, local files, and optional external publishing outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local memory keywords, call authenticated SkillHub CLI commands, and optionally write or publish reports to configured destinations.]

## Skill Version(s):

7.0.1 (source: frontmatter, evidence release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
