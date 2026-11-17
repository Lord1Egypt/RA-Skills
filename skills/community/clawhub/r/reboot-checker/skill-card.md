## Description:

Detect unexpected system reboots and alert when the system comes back online. Tracks boot history and flags suspicious restarts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hostilespider](https://clawhub.ai/user/hostilespider)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check whether a host rebooted since the last recorded boot time and to surface reboot status in startup, cron, or heartbeat workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom state or history paths can write reboot state into unexpected or shared writable locations.

Mitigation: Run the script as an unprivileged user, prefer the default home-directory state files, and do not pass custom --state, STATE_FILE, or HISTORY_FILE values from untrusted sources.

Risk: Running the reboot check as root from cron can broaden the impact of file writes.

Mitigation: Schedule the check under an unprivileged account unless elevated privileges are explicitly required by the deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [Plain text status lines or JSON status objects, with bash command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes reboot state and history files locally and exits nonzero when it detects a reboot.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
