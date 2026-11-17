## Description:

Quality audit for OpenClaw skill files that scores SKILL.md files on clarity, completeness, authenticity, examples, and freshness, checks references and frontmatter, and produces a local markdown review log without editing skill files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crispyangles](https://clawhub.ai/user/crispyangles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to review OpenClaw skill files for documentation quality, broken references, stale links, and frontmatter issues before release or during periodic maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans SKILL.md files in the workspace and appends results to a local report.

Mitigation: Run it only in workspaces where reviewing skill documentation is intended, and confirm the report path before scheduled use.

Risk: The optional link freshness check can make outbound HTTP requests with curl.

Mitigation: Leave the optional link check disabled unless outbound network requests are acceptable in the operating environment.

Risk: Quality scores and findings may be incomplete or subjective.

Mitigation: Use the report as review guidance and have a maintainer approve any follow-up edits before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/crispyangles/skills/sparkforge-skill-refiner)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and a local review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends review results to memory/skill-refiner-log.md; optional link freshness checks may make outbound HTTP requests with curl.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
