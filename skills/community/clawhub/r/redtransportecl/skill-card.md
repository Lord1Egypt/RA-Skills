## Description:

Uses the `red-transporte` CLI to query stops, routes, real-time predictions, local GTFS data, geospatial utilities, and transit trip planning for Chile's Red de Transporte system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiroak](https://clawhub.ai/user/iiroak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and transit-data users use this skill to operate the `red-transporte` CLI and local API for Chilean public transit lookups, GTFS refreshes, real-time stop predictions, nearby stop discovery, and route planning.

### Deployment Geography for Use:

Chile

## Known Risks and Mitigations:

Risk: The documented `pip install ".[all]"` command can install an unintended local Python project if run from an arbitrary workspace.

Mitigation: Install only in a trusted virtual environment from a verified `red-transporte` source, and avoid running the install command from unrelated directories.

Risk: Coordinates entered for nearby stop, station, and routing commands may reveal sensitive location information.

Mitigation: Use the minimum necessary coordinate precision, avoid unnecessary logging or sharing of coordinates, and handle command output as location-sensitive data.

## Reference(s):

- [RedTransporteAPI on ClawHub](https://clawhub.ai/iiroak/skills/redtransportecl)
- [RED fare reference](https://www.red.cl/tarifas-y-recargas/conoce-las-tarifas/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, CLI, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can recommend JSON output workflows through the CLI's `--json` flag.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
