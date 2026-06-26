## Description: <br>
Detect unexpected system reboots and alert when the system comes back online. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hostilespider](https://clawhub.ai/user/hostilespider) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check a local host for unexpected reboots, view boot history, and integrate reboot alerts into cron or heartbeat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reboot checker writes local state and history files and may be scheduled through cron or heartbeat systems. <br>
Mitigation: Review the shell script before scheduling it, run it as a normal user when possible, and use explicit state, history, and log paths for integrations. <br>
Risk: Resetting state marks the current boot as known and removes the stored reboot marker. <br>
Mitigation: Use the reset option only when intentionally accepting the current boot as the baseline. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text status lines or JSON from the Bash script, with Markdown guidance in the skill instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reboot state and history to user-configurable local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
