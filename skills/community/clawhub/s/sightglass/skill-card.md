## Description: <br>
Monitors AI coding agents to track dependency choices, classify discovery methods, flag risks, and reveal biases and missed alternatives in a project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidgeorgehope](https://clawhub.ai/user/davidgeorgehope) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use Sightglass to monitor AI coding agent sessions, analyze dependency decisions, classify discovery methods, and surface supply-chain risks, missed alternatives, and bias indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script installs the external @sightglass/cli package globally without a pinned version. <br>
Mitigation: Inspect and pin the npm package before installing, especially on private, regulated, or sensitive codebases. <br>
Risk: The skill can start a persistent watcher that monitors agent sessions, file changes, package installs, and tool calls. <br>
Mitigation: Run the watcher only in intended project directories, confirm where session data is stored, and stop the watcher when monitoring is no longer needed. <br>
Risk: Authenticated analysis can sync or push data to sightglass.dev, and the scope of cloud sync is not clearly established in the evidence. <br>
Mitigation: Confirm collection and upload behavior, disable cloud sync or auto-push where required, and avoid use with sensitive projects until approved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davidgeorgehope/sightglass) <br>
- [Sightglass Service](https://sightglass.dev) <br>
- [Publisher Profile](https://clawhub.ai/user/davidgeorgehope) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Text, JSON, or Markdown analysis reports with shell commands for setup and session hooks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run a persistent watcher and can push analysis to sightglass.dev when configured or invoked with push behavior.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
