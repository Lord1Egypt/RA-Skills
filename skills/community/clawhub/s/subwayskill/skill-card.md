## Description:

Fetch NYC subway departure times for subway, commute, next-train, and NYC transit schedule questions across NYC subway and SIR lines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyluke](https://clawhub.ai/user/nyluke)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to answer NYC subway departure questions by running the subwayskill CLI for default or requested stations, lines, directions, and times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation uses a mutable upstream Go module reference.

Mitigation: Install from a pinned, reviewed version or checksum-backed release instead of an unpinned latest reference.

Risk: The CLI makes outbound requests to MTA-related endpoints and downloads schedule data.

Mitigation: Run the skill only where those network calls are expected, and consider endpoint allowlisting for automated environments.

Risk: The CLI writes GTFS cache files under the user's cache directory.

Mitigation: Run with normal user privileges and resource limits, and monitor or clear `~/.cache/subwayskill/` where cache persistence matters.

## Reference(s):

- [ClawHub SubwaySkill listing](https://clawhub.ai/nyluke/skills/subwayskill)
- [Publisher profile](https://clawhub.ai/user/nyluke)
- [Skill homepage](https://github.com/nyluke/subwayskill)
- [MTA static GTFS API](https://api.mta.info/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text subway departure summaries or structured JSON from the subwayskill CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include realtime or scheduled source labels, station names, routes, directions, departure times, and minutes away.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
