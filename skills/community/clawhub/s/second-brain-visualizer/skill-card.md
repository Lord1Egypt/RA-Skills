## Description: <br>
Reads a raw idea stream from a local second-brain ledger, turns notes into structured atoms, clusters them by intent with an OpenClaw-routed LLM, and renders the resulting patterns in a React visualizer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[highnoonoffice](https://clawhub.ai/user/highnoonoffice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to parse a personal markdown idea ledger, generate intent-based clusters, and view emerging signals, tensions, and absences in a dashboard. It is intended for users who want to analyze their own private idea stream rather than maintain a traditional note taxonomy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow centralizes raw personal notes and selected private-channel content. <br>
Mitigation: Use a dedicated low-sensitivity ledger or channel, avoid secrets and regulated data in atoms, and review the accumulated corpus before clustering. <br>
Risk: The clusterer sends the atom corpus to the configured OpenClaw gateway and may reach a remote endpoint if the gateway host is changed. <br>
Mitigation: Keep the gateway host set to 127.0.0.1 or localhost unless a remote endpoint is deliberately trusted, and verify OpenClaw's LLM routing before running clustering. <br>
Risk: Slack, Telegram, and gateway credential files are stored locally under ~/.openclaw/credentials. <br>
Mitigation: Restrict filesystem access to credential files, use dedicated credentials where possible, and rotate credentials if they are exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/highnoonoffice/second-brain-visualizer) <br>
- [Publisher Profile](https://clawhub.ai/user/highnoonoffice) <br>
- [Homepage](https://github.com/highnoonoffice/hno-skills) <br>
- [Setup Guide](references/setup.md) <br>
- [Install Guide](references/install.md) <br>
- [Ingestion Guide](references/ingestion.md) <br>
- [Parser Script](references/parser.js) <br>
- [Clustering Script](references/cluster.js) <br>
- [Visualizer Component](references/component.tsx) <br>
- [Sample Atom Ledger](references/sample-ledger.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript, TypeScript React, shell commands, and JSON data schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local atom JSON, cluster JSON, and a React/D3 visual graph when installed in a compatible dashboard.] <br>

## Skill Version(s): <br>
1.6.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
