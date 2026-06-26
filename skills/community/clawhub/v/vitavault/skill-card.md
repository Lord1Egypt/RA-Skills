## Description: <br>
VitaVault iOS app integration - sync Apple Health data directly to your AI agent. Auto-setup webhook, token generation, and HTTPS exposure. Works with any iPhone, no Mac required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrandonS7](https://clawhub.ai/user/BrandonS7) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
External users and developers use this skill to connect VitaVault iOS Apple Health exports to an OpenClaw agent, receive local webhook syncs, import manual exports, and generate summaries or briefings from synced health data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish and persist an HTTPS webhook that receives sensitive health data. <br>
Mitigation: Require explicit approval before tunnel or service setup, set a strong VITAVAULT_SYNC_TOKEN, and do not run the webhook unauthenticated. <br>
Risk: Health data may be stored on the agent host and exposed through logs, local files, or a misconfigured tunnel. <br>
Mitigation: Limit filesystem access to ~/vitavault/data/, protect the sync token, review tunnel configuration, and avoid sharing generated URLs or credentials. <br>
Risk: scripts/query.py uses a remote API endpoint even though the skill text emphasizes local-only data flow. <br>
Mitigation: Review scripts/query.py before use, set VITAVAULT_API_URL only to a trusted private endpoint, or prefer the local import and summary scripts when remote access is not intended. <br>


## Reference(s): <br>
- [VitaVault Data Types](references/data-types.md) <br>
- [VitaVault Export Schema](references/schema.md) <br>
- [VitaVault Developer Documentation](https://vitavault.io/developers/) <br>
- [VitaVault Website](https://vitavault.io) <br>
- [VitaVault on TestFlight](https://testflight.apple.com/join/A4G27HBt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local health-data JSON files under ~/vitavault/data/ and run a persistent HTTPS webhook when configured.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
