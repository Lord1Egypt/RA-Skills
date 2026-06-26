## Description: <br>
Fetch personalized developer news digests from Snapbyte External API with API-key auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onatm](https://clawhub.ai/user/onatm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to retrieve their Snapbyte digest configurations, latest digests, digest history, individual digests, and digest items, then present results as markdown or raw JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retrieves user-scoped Snapbyte digest data using SNAPBYTE_API_KEY. <br>
Mitigation: Install it only when digest retrieval is intended, and keep the API key private, current, and scoped according to Snapbyte guidance. <br>
Risk: SNAPBYTE_BASE_URL can redirect requests to a different Snapbyte-compatible endpoint. <br>
Mitigation: Leave SNAPBYTE_BASE_URL unset unless the alternate endpoint is trusted. <br>
Risk: The quickstart includes an optional cron workflow that can run digest retrieval on a schedule. <br>
Mitigation: Add the cron job only when recurring automatic digest delivery is desired, and review scheduled runs periodically. <br>


## Reference(s): <br>
- [Snapbyte API Documentation](https://api.snapbyte.dev/docs) <br>
- [Snapbyte API Base URL](https://api.snapbyte.dev) <br>
- [Snapbyte Digest API Quickstart](references/quickstart.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/onatm/snapbyte-digest-api) <br>
- [Publisher Profile](https://clawhub.ai/user/onatm) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown by default, with optional raw JSON output and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SNAPBYTE_API_KEY for authenticated read-only API requests; SNAPBYTE_BASE_URL can override the default endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
