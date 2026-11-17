## Description:

Audits a ClawHub skill folder before publishing, checking metadata alignment, missing required fields, potential secret exposure, file limits, license and pricing conflicts, trigger quality, and stale guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solidstate](https://clawhub.ai/user/solidstate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill before a ClawHub publish or release to audit a skill folder for blockers and warnings that could hide or reject the release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be misused as an install-safety review for third-party skills, which its own instructions and security guidance say is outside scope.

Mitigation: Use it for local pre-publish checks, and use a dedicated install-vetting workflow before installing third-party skills.

Risk: The report template includes Solid State branding, which may affect how users perceive audit neutrality.

Mitigation: Review generated reports before sharing them and treat branding as publisher attribution rather than independent certification.

## Reference(s):

- [Publish Audit on ClawHub](https://clawhub.ai/solidstate/skills/publish-audit)
- [Solid State homepage](https://solidstate.cc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style audit report with pass, warn, and blocker lines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a READY or FIX FIRST verdict, plus a publish command when the audit is clean.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
