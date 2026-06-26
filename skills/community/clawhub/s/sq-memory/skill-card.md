## Description: <br>
Enables OpenClaw agents to store, recall, update, list, and forget persistent hierarchical memories across sessions via the SQ protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wbic16](https://clawhub.ai/user/wbic16) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use SQ Memory to give OpenClaw agents durable memory for user preferences, conversation history, long-running project context, and multi-agent coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable agent memory can retain sensitive user, project, or organizational information beyond the current session. <br>
Mitigation: Do not store secrets or sensitive personal or regulated data; review and delete stored memories regularly. <br>
Risk: Weak memory scoping, prefix listing, or query-string storage issues could expose private memories to unintended agents or users. <br>
Mitigation: Use separate namespaces per user and agent, prefer local or HTTPS endpoints with verified authentication, and patch or account for the known scoping and query-string issues before private workflows. <br>
Risk: Self-hosted deployments may run without authentication by default. <br>
Mitigation: Keep self-hosted endpoints local or behind network controls, and add HTTPS plus authentication before exposing the service beyond a trusted machine. <br>


## Reference(s): <br>
- [ClawHub SQ Memory release page](https://clawhub.ai/wbic16/sq-memory) <br>
- [Quick Start](QUICKSTART.md) <br>
- [Self-Hosted SQ Setup](SELF-HOSTED.md) <br>
- [SQ source repository](https://github.com/wbic16/SQ) <br>
- [SQ hosted documentation](https://mirrorborn.us/help.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands, guidance] <br>
**Output Format:** [Plain text and JSON-like tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and retrieves durable text memories by endpoint, phext, namespace, and coordinate; documentation states a maximum of 1 MB per coordinate.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, skill.json, package.json, and index.js) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
