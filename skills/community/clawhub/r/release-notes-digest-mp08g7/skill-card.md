## Description:

Turn a repository's merged pull requests and release tags into a concise, reviewer-friendly release note, with per-item provenance links and an explicit "unattributed" section for entries that cannot be mapped to a change owner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use the skill to prepare concise release notes from merged pull requests and release tags, then review linked changes before approving a release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean scan does not guarantee zero risk.

Mitigation: Consider whether the skill suits the intended use before installing.

Risk: Long release histories are truncated, so a digest may omit older changes.

Mitigation: Check the stated truncation and follow the source links when reviewing release coverage.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cindypapa/skills/release-notes-digest-mp08g7)
- [Publisher profile](https://clawhub.ai/user/cindypapa)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown summary with grouped change bullets, source links, and an unattributed section]

**Output Parameters:** [1D: one digest between a baseline revision and a target revision]

**Other Properties Related to Output:** [Quotes change subjects, links each item to its source, and states when a long history has been truncated.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
