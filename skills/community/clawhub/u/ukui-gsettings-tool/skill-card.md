## Description: <br>
A skill for exporting, inspecting and applying UKUI desktop gsettings presets, with fine-grained get/set support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizhuoan](https://clawhub.ai/user/lizhuoan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and desktop administrators use this skill to export, inspect, synchronize, and apply UKUI or GNOME gsettings presets across user environments. It also supports targeted reads and writes for individual schema keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying presets changes the current user's desktop gsettings. <br>
Mitigation: Review preset JSON before applying it and export the current settings first when rollback may be needed. <br>
Risk: Exported presets can contain private paths, usernames, or machine-specific values. <br>
Mitigation: Redact private or host-specific values before sharing exported presets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lizhuoan/ukui-gsettings-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON files, shell commands, configuration] <br>
**Output Format:** [Command-line text and gsettings preset JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and gsettings on a UKUI or GNOME-compatible desktop session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
