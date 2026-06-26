## Description: <br>
Synchronizes workspace heartbeat state with memory logs, work-session entries, and daily heartbeat reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents maintaining OpenClaw workspaces use this skill to log work sessions, synchronize heartbeat state, and generate summaries from workspace memory and task files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled installer can publish the package through the user's ClawHub account during what appears to be a local install. <br>
Mitigation: Install through the normal ClawHub flow when possible, and review install.sh before running the bundled installer. <br>
Risk: Heartbeat logs are persistent workspace memory and may capture sensitive work details. <br>
Mitigation: Avoid logging secrets and periodically review files written under the workspace memory directory. <br>
Risk: The installer creates or overwrites local configuration. <br>
Mitigation: Review the generated configuration path and contents before relying on automated heartbeat syncing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/utopiabenben/workspace-heartbeat-integration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Command-line text, Markdown reports, JSON reports, and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes heartbeat state, daily memory logs, and optional user configuration in local workspace paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
