## Description: <br>
Manages Tencent Cloud Lighthouse instances through mcporter and a Lighthouse MCP server, including setup, instance queries, monitoring, firewall changes, snapshots, and remote command execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Tencent Cloud Lighthouse servers from an agent, including setup, inventory, monitoring, alerts, firewall rules, snapshots, and remote commands. It is scoped to Lighthouse rather than CVM or other cloud server types. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for powerful Tencent Cloud credentials and stores them locally for an external MCP server. <br>
Mitigation: Use a dedicated least-privileged Tencent CAM key limited to the needed Lighthouse actions, and delete or rotate the key when finished. <br>
Risk: The MCP workflow can run remote commands and change firewall settings on Lighthouse instances. <br>
Mitigation: Confirm every remote-command and firewall action before execution, and verify the target Region and InstanceId before running commands. <br>
Risk: Setup installs or invokes external Node packages for mcporter and the Lighthouse MCP server. <br>
Mitigation: Verify the mcporter and lighthouse-mcp-server packages before use and run the setup in a least-privileged environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason-aka-chen/tencent-lighthouse-chen) <br>
- [Tencent Cloud CAM API key management](https://console.cloud.tencent.com/cam/capi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON arguments, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use mcporter with JSON output and a local mcporter configuration file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
