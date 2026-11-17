## Description:

Scans installed skills for version drift and delisted publishers, producing a fleet health report with items that need attention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ordo-tech](https://clawhub.ai/user/ordo-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit installed ClawHub or OpenClaw skills for outdated versions or delisted listings after installation, during periodic hygiene checks, or after security advisories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The released free workflow requests broader authority than its documented two checks require.

Mitigation: Install only after reviewing the requested read, write, web_fetch, and web_search access; prefer a version that removes unused write and web_search permissions from the free workflow.

Risk: The skill inventories installed skills and contacts ClawHub to check versions and delisting status.

Mitigation: Run it only where installed skill names, versions, publishers, and related listing checks are acceptable to process against public ClawHub pages.

Risk: Generated reports may include a commercial upgrade link.

Mitigation: Review reports before sharing or archiving them in security records, and remove promotional content when it is not appropriate for operational output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ordo-tech/skills/skill-fleet-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/ordo-tech)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown fleet health report with status lines and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free workflow covers version drift and delisted-skill checks; reports may include a commercial upgrade link.]

## Skill Version(s):

1.1.3 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
