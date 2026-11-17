## Description:

Run the installed red-crawler CLI for Xiaohongshu contact discovery. Requires the red-crawler command and Playwright browser runtime; not instruction-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[batxent](https://clawhub.ai/user/batxent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run installed red-crawler workflows for Xiaohongshu creator and contact discovery, browser login state capture, scheduled collection, weekly reports, and contactable-creator exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configurable runner_command can broaden command execution beyond the expected crawler wrapper.

Mitigation: Use the skill only in a dedicated workspace, keep runner_command fixed to the expected red-crawler command, and do not allow untrusted prompts or workflows to set it.

Risk: Browser authentication values and Playwright storage-state files may appear in returned output, job files, or logs.

Mitigation: Avoid supplying browser_auth unless this exposure is acceptable, keep storage-state files private, and review generated job files and logs before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/batxent/skills/rednote-contacts)
- [Publisher profile](https://clawhub.ai/user/batxent)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [JSON action results with command strings, artifact paths, stdout/stderr text, and optional background job state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Crawler actions may produce CSV exports, JSON reports, job state files, heartbeat files, and stdout/stderr logs.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
