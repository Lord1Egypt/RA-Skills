## Description:

Guides publication of a validated GTFS Schedule ZIP by checking exact public feed bytes, triaging validator findings, rerunning after corrections, and reporting release evidence and limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powmcp](https://clawhub.ai/user/powmcp)

### License/Terms of Use:

MIT-0

## Use Case:

Transit agency staff, developers, and operations teams use this skill to gate GTFS Schedule releases, compare same-agency baseline and revised feeds, and preserve validation evidence before publishing or reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can pull changing third-party code through an npx install command.

Mitigation: Install only from a trusted PowMCP source and prefer a pinned version or reviewed commit before running the install command.

Risk: The workflow sends direct public GTFS Schedule URLs to a remote service.

Mitigation: Use only public feeds intended for validation and do not provide private feeds, authenticated links, credentials, or sensitive query strings.

Risk: Automated validation can be mistaken for full release approval.

Mitigation: Keep human timetable review and distributor-specific acceptance review separate from the GTFS Feed Check result.

## Reference(s):

- [GTFS Feed Check reference](references/gtfs-feed-check.md)
- [GTFS Feed Check app](https://powmcp.com/apps/gtfs-feed-check/)
- [GTFS validation guidance](https://gtfs.org/getting-started/validate/)
- [Canonical GTFS Validator rules](https://gtfs-validator.mobilitydata.org/rules.html)
- [Canonical GTFS Validator releases](https://github.com/MobilityData/gtfs-validator/releases)
- [ClawHub skill page](https://clawhub.ai/powmcp/skills/publish-service-change-feed)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, command snippets, and structured validation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses measured GTFS Feed Check results when available and reports coverage limits without treating automated validation as human service approval.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata version 2026.09.10+gtfs-feed-check@0.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
