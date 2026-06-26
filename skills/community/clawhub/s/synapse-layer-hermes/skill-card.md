## Description: <br>
Zero-Knowledge persistent memory layer for Hermes Agent. Provides encrypted cross-session memory, Trust Quotient (TQ) scoring, and automatic recall across ALL channels (Telegram, WhatsApp, CLI, Discord). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafacpti23](https://clawhub.ai/user/rafacpti23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Hermes Agent operators use this skill to configure Synapse Layer as persistent encrypted memory across chat and CLI channels. It guides recall, save, search, health-check, and REST fallback workflows for the Synapse Layer MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs broad persistent storage of cross-channel conversation memory, including categories that may include credentials or sensitive infrastructure details. <br>
Mitigation: Configure the agent not to save secrets, API keys, tokens, regulated personal data, or sensitive infrastructure details; use a dedicated secret manager for credentials. <br>
Risk: The integration requires a SYNAPSE_TOKEN bearer credential for the remote Synapse Layer service. <br>
Mitigation: Store the token outside prompts and source files, scope it narrowly where possible, rotate it regularly, and revoke it if exposed. <br>
Risk: MCP connectivity may be unreliable when Hermes encounters the documented reconnect loop. <br>
Mitigation: Use the documented REST JSON-RPC fallback, verify health-check responses, and review recalled memories before relying on low-confidence results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rafacpti23/synapse-layer-hermes) <br>
- [Synapse Layer homepage](https://synapselayer.org) <br>
- [Synapse Layer documentation](https://synapselayer.org/docs) <br>
- [Synapse Layer Forge dashboard](https://forge.synapselayer.org/forge) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, API calls] <br>
**Output Format:** [Markdown with YAML, shell, and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SYNAPSE_TOKEN bearer credential and access to the external Synapse Layer MCP/REST service.] <br>

## Skill Version(s): <br>
1.1.9-b (source: ClawHub release metadata; artifact frontmatter reports 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
