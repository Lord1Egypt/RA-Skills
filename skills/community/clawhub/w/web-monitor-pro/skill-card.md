## Description: <br>
Web Monitor helps agents set up and manage local web-page monitors for content changes, price drops, stock availability, custom conditions, visual diffs, price comparisons, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jakes420](https://clawhub.ai/user/jakes420) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and external users use this skill to watch URLs for page changes, price drops, restocks, and custom text or price conditions, then review status, history, reports, visual diffs, or configured webhook alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitored URLs and page snapshots are stored locally under ~/.web-monitor. <br>
Mitigation: Monitor only URLs appropriate for local storage, set WEB_MONITOR_DIR when isolation is needed, and remove monitors or stored snapshots that are no longer required. <br>
Risk: Configured webhooks send monitored URLs and change details to external endpoints. <br>
Mitigation: Use trusted webhook destinations and avoid webhook alerts for pages or changes that contain sensitive information. <br>
Risk: Debug and feedback output can include local system details or prior feedback text. <br>
Mitigation: Review debug and feedback output before sharing it outside the local environment. <br>


## Reference(s): <br>
- [Web Monitor Examples](artifact/references/examples.md) <br>
- [ClawHub Listing](https://clawhub.ai/jakes420/web-monitor-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, files, guidance] <br>
**Output Format:** [CLI text, JSON exports and imports, Markdown-style guidance, HTML diffs, and local monitor configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores monitor configuration, snapshots, screenshots, feedback logs, and generated console or diff files under ~/.web-monitor unless WEB_MONITOR_DIR is set; configured webhooks send JSON event payloads.] <br>

## Skill Version(s): <br>
3.5.0 (source: server release metadata, skill frontmatter, and monitor.py VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
