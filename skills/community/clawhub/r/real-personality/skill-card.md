## Description:

REAL Personality Test scans a user's social media behavior, including posts, likes, saves, and follows, and classifies the account into one of 16 data-driven personality types with a match score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sophie-xin9](https://clawhub.ai/user/sophie-xin9)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect data from a user's own logged-in social media accounts and generate a REAL personality profile. The output includes a four-letter type code, match score, detailed report, and optional shareable card.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly collects sensitive social-media activity from logged-in accounts and stores raw data locally.

Mitigation: Confirm each platform and data category before scanning, run it only against accounts the user intends to analyze, and delete generated raw data after use unless retention is intentional.

Risk: The skill uses logged-in browser sessions to access supported social platforms.

Mitigation: Use a dedicated browser profile where practical, review the account context before execution, and stop if the user is not comfortable with the requested collection scope.

Risk: The skill can bootstrap an unpinned browser-control dependency.

Mitigation: Avoid the unpinned auto-clone path; install and review a trusted ManoBrowser version before running collection steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sophie-xin9/skills/real-personality)
- [Publisher profile](https://clawhub.ai/user/sophie-xin9)
- [Artifact README](artifact/README.md)
- [REAL type system](artifact/types/type_system.md)
- [Example REAL report](artifact/examples/xiaokai_real_report.md)
- [ManoBrowser dependency](https://github.com/ClawCap/ManoBrowser)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown report with JSON data files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a four-letter REAL type code, match score, detailed report, and optional shareable card; may save raw collection data locally.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
