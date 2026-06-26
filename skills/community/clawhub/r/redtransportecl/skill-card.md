## Description: <br>
Uses the `red-transporte` CLI to query Chile Red de Transporte stops, routes, local GTFS data, real-time predictions, geospatial utilities, and route-planning API endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iiroak](https://clawhub.ai/user/iiroak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and transit automation agents use this skill to run `red-transporte` commands for Chile public-transit lookup, GTFS maintenance, live stop predictions, and coordinate-based trip planning. <br>

### Deployment Geography for Use: <br>
Chile <br>

## Known Risks and Mitigations: <br>
Risk: Coordinate-based queries can expose sensitive home, work, or travel-pattern information if shared in logs or shell history. <br>
Mitigation: Treat exact coordinates as private and avoid storing or sharing them in logs, transcripts, or command history. <br>
Risk: The local HTTP server exposes transit API endpoints if bound or proxied beyond the local machine. <br>
Mitigation: Keep the server local by default; add authentication, TLS, and access controls before any public exposure. <br>
Risk: The skill depends on an external `red-transporte` binary or package outside the skill artifact. <br>
Mitigation: Install only from a trusted source and verify the package before using the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/iiroak/redtransportecl) <br>
- [RED fare reference](https://www.red.cl/tarifas-y-recargas/conoce-las-tarifas/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, CLI examples, curl examples, and JSON-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can emit raw JSON with `--json`; local GTFS data is required for static transit queries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
