## Description: <br>
Read-only access to UniFi Network data for device inventory, network configuration, client information, alerts, health status, firmware status, bandwidth summaries, and topology export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbojer](https://clawhub.ai/user/mbojer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and infrastructure engineers use this skill to inspect UniFi Network sites, troubleshoot device and client connectivity, and generate concise network documentation from read-only API data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive UniFi infrastructure details through API responses, local cache files, and topology exports. <br>
Mitigation: Use a dedicated read-only UniFi API key, keep ~/.clawdbot/credentials and ~/.clawdbot/cache private, and avoid writing topology exports into synced or shared folders. <br>
Risk: Local cache clearing has under-scoped path handling when given untrusted or path-like cache keys. <br>
Mitigation: Use cache_clear.sh only with --status, --all, or known cache keys until its path handling is fixed. <br>


## Reference(s): <br>
- [UniFi API Endpoint Reference](artifact/references/endpoints.md) <br>
- [ClawHub skill page](https://clawhub.ai/mbojer/unifi-os) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON or Markdown network reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only UniFi API calls, local credential configuration, and cached API responses; topology export can write a Markdown file when an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
