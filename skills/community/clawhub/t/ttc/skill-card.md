## Description:

Real-time Toronto transit for bus and streetcar arrivals, vehicle tracking, alerts, and stop search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasygu](https://clawhub.ai/user/lucasygu)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and AI agents use this skill to query Toronto Transit Commission bus and streetcar arrivals, vehicle positions, service alerts, nearby stops, route status, and stop search results from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global installation may replace or delete an existing ~/.claude/skills/ttc path.

Mitigation: Back up or inspect ~/.claude/skills/ttc before installing globally, and review the install script behavior before deployment.

Risk: The macOS nearby command can request device location permission.

Mitigation: Use explicit latitude and longitude coordinates instead of ttc nearby auto-detection when location permission is not acceptable.

Risk: The security scan verdict is suspicious and recommends review before install.

Mitigation: Prefer an updated release that avoids destructive postinstall replacement, uses safer temporary files, and refreshes vulnerable dependencies.

## Reference(s):

- [TTC CLI source repository](https://github.com/lucasygu/ttc-cli)
- [ClawHub TTC CLI skill page](https://clawhub.ai/lucasygu/skills/ttc)
- [TTC GTFS-RT feed endpoint](https://bustime.ttc.ca/gtfsrt)
- [TTC broad alerts GTFS-RT endpoint](https://gtfsrt.ttc.ca)
- [Open Toronto GTFS dataset](https://open.toronto.ca/dataset/merged-gtfs-ttc-routes-and-schedules/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Terminal text or JSON from ttc CLI commands, often summarized as Markdown by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [All commands support --json for programmatic output.]

## Skill Version(s):

0.1.7 (source: server release metadata and package.json; SKILL.md frontmatter lists 0.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
