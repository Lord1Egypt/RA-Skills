## Description:

SkillWiki helps agents fetch structured ClawHub skill metadata and produce safety, quality, and capability reviews before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skinapi2025](https://clawhub.ai/user/skinapi2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use SkillWiki to inspect ClawHub skills before installation, compare candidate skills, and generate concise security and capability reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviews depend on a currently served remote ClawHub package, so audit results may change if the remote package changes.

Mitigation: Pin the intended release version and compare server-provided hashes or fingerprints before relying on a review.

Risk: The fetch workflow processes downloaded ZIP archives, which can undermine audit integrity if package contents are not verified.

Mitigation: Use only trusted ClawHub download endpoints, verify package digests, and enforce archive size and path constraints before extraction.

Risk: Generated skill reviews can be incomplete or misleading if fetched content is truncated or unavailable.

Mitigation: Treat reports as triage, confirm important findings against the extracted JSON and server security evidence, and review manually before installing.

## Reference(s):

- [ClawHub SkillWiki release page](https://clawhub.ai/skinapi2025/skills/skillwiki)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown review reports with optional JSON extraction output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports language preference configuration through SKILLWIKI_LANG.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
