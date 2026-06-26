## Description: <br>
Monitors public website pages for content changes, compares snapshots, and reports meaningful updates for prices, regulations, job postings, news, and technical documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to define public website monitoring tasks, run periodic checks, compare stored snapshots, and export change data for downstream analysis or notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes anti-bot evasion guidance, proxy rotation, CAPTCHA handling, and cookie-based scraping beyond normal public-page monitoring. <br>
Mitigation: Use it only for sites the user is authorized to monitor; avoid proxy rotation, CAPTCHA bypass, and session-cookie scraping; honor robots.txt and applicable site terms. <br>
Risk: Periodic website checks can create excessive request load or trigger blocking when frequency and target scope are not controlled. <br>
Mitigation: Set explicit monitoring frequency limits, use backoff after 403 or 429 responses, and document approved targets and notification destinations before deployment. <br>
Risk: Local snapshots may retain sensitive or regulated page content in $HOME/.web-monitor. <br>
Mitigation: Set retention limits, restrict local file permissions, scrub unnecessary sensitive data, and periodically delete stale snapshots and logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/web-data-monitor-claw) <br>
- [Monitoring rules](references/monitoring-rules.md) <br>
- [Extraction templates](references/extraction-templates.md) <br>
- [Anti-detection strategies](references/anti-detection.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with bash examples; script commands return JSON status objects and local snapshot files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores tasks, logs, and snapshots under WEB_MONITOR_DATA_DIR or $HOME/.web-monitor.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
