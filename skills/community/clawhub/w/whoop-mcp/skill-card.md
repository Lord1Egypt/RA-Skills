## Description: <br>
Connect an MCP-compatible agent to local WHOOP recovery, sleep, strain, HRV, cycles, and workouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and MCP users use this skill to install, configure, and troubleshoot WHOOP MCP for agent access to WHOOP recovery, sleep, strain, HRV, cycles, and workout data while preserving explicit consent and privacy boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WHOOP OAuth tokens and private wellness data may be exposed through local files, logs, or raw provider payloads. <br>
Mitigation: Keep ~/.whoop-mcp token files private, do not print secrets or private user data, and prefer summarized results unless raw payloads are explicitly requested. <br>
Risk: The skill depends on the third-party whoop-mcp-unofficial package and can connect an agent to live WHOOP data. <br>
Mitigation: Install only if the package is trusted, run setup and authentication intentionally, review OAuth scopes, and prefer connection_status, manifest, doctor, privacy_audit, or dry-run surfaces before live provider calls. <br>
Risk: WHOOP data can be mistaken for professional medical, legal, financial, or platform-policy advice. <br>
Mitigation: Keep user consent explicit and present outputs as wellness-data assistance rather than professional advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davidmosiah/whoop-mcp) <br>
- [WHOOP MCP Repository](https://github.com/davidmosiah/whoop-mcp) <br>
- [WHOOP Connector Docs](https://wellness.delx.ai/connectors/whoop) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include setup, authentication, privacy-boundary, and troubleshooting guidance for MCP-compatible clients.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
