## Description:

Skane public transport trip planner for Skanetrafiken that plans bus and train journeys with real-time delays, station and address lookup, landmarks, and cross-border trips to Copenhagen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rezkam](https://clawhub.ai/user/rezkam)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to search Skanetrafiken locations, resolve ambiguous stations or addresses, and plan public-transit trips in Skane with real-time timing, delay, platform, walking, and disruption details.

### Deployment Geography for Use:

Global; transit coverage is focused on Skane, Sweden, with supported cross-border trips to Copenhagen.

## Known Risks and Mitigations:

Risk: Trip searches send submitted locations or coordinates to Skånetrafiken.

Mitigation: Avoid submitting sensitive addresses or coordinates unless the user accepts that disclosure.

Risk: Installing with a moving latest tag can change the installed code unexpectedly.

Mitigation: Prefer a pinned installer version when installing the skill.

Risk: The bundled shell scripts use temporary files that are not fully hardened for hostile shared machines.

Mitigation: Run the scripts without elevated privileges and avoid using them on untrusted shared systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rezkam/skills/skanetrafiken)
- [Skånetrafiken Points API endpoint](https://www.skanetrafiken.se/gw-tps/api/v2/Points)
- [Skånetrafiken Journey API endpoint](https://www.skanetrafiken.se/gw-tps/api/v2/Journey)
- [Agent Skills compatibility reference](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and formatted trip-planning results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces location-search fields, journey options, walking distances, local times, delay indicators, platform details, transfer counts, and disruption notices.]

## Skill Version(s):

1.2.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
