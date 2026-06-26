## Description: <br>
Discover, list, and search WhatsApp groups from Baileys session data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcosRippel](https://clawhub.ai/user/MarcosRippel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to discover WhatsApp groups available to an OpenClaw bot account, search group names, retrieve group IDs, and optionally add disabled group entries to OpenClaw configuration for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local WhatsApp/Baileys session data and can expose group IDs and names. <br>
Mitigation: Install only when the agent is allowed to inspect the bot account's WhatsApp session data; use list, search, and get-id for read-only discovery. <br>
Risk: The sync command edits openclaw.json by adding newly discovered groups. <br>
Mitigation: Run sync only intentionally, then review the added disabled group entries before enabling any group. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, configuration] <br>
**Output Format:** [JSON command output with optional openclaw.json updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads Baileys sender-key, store, and contacts files from the local OpenClaw state directory; the sync command writes disabled group entries to openclaw.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
