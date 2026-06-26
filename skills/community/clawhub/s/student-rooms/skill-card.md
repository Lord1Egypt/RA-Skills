## Description: <br>
Search, scan, and monitor student accommodation availability across Yugo and Aparto providers with semester filters, booking probes, and notification options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gonzalopezgil](https://clawhub.ai/user/gonzalopezgil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to discover student accommodation, compare availability and pricing, probe booking options, and monitor for new matching rooms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alerts can be sent to webhook, Telegram, or OpenClaw destinations. <br>
Mitigation: Use stdout mode when results should stay local, and confirm the destination and expected payload before enabling external notifications. <br>
Risk: Watch mode and create_job_on_match can create local monitoring state or scheduled follow-up jobs. <br>
Mitigation: Confirm the monitoring duration, how to stop it, and how to remove saved state or scheduled jobs before enabling those modes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gonzalopezgil/student-rooms) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, configuration snippets, and JSON result examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured JSON output is recommended for discovery, scanning, booking probes, and match testing.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
