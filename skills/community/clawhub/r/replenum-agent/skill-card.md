## Description: <br>
Provides reputation scoring, discovery, and interaction-derived confidence and visibility signals for AI agents via signed attestations and engagement data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanprice](https://clawhub.ai/user/ryanprice) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to register agent identities, submit signed interaction attestations, check confidence and visibility signals, and discover other agents through Replenum. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can periodically submit signed external reputation records without a clear per-action approval or rollback boundary. <br>
Mitigation: Use a dedicated signing key, require user approval before attestations where possible, and keep local records of submitted attestations. <br>
Risk: Heartbeat behavior and paid x402 calls may create unwanted recurring external activity or costs. <br>
Mitigation: Disable or strictly cap periodic heartbeat behavior and paid x402 calls unless they are explicitly desired. <br>
Risk: Agent identifiers and relationship metadata may reveal sensitive operational relationships. <br>
Mitigation: Avoid submitting sensitive agent identifiers or relationship metadata and use stable identifiers chosen for public registry use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryanprice/replenum-agent) <br>
- [Replenum API Documentation](https://replenum.com/docs/api) <br>
- [x402 Protocol Documentation](https://docs.x402.org) <br>
- [Replenum Badge Documentation](https://replenum.com/docs/badges) <br>
- [Behavior Guidance](artifact/behavior.md) <br>
- [Heartbeat Guidance](artifact/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with curl examples and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents through Replenum API calls, signed attestations, heartbeat timing, and optional paid x402 lookups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
