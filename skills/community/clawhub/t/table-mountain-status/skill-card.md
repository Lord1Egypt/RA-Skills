## Description: <br>
Fetches official Table Mountain Aerial Cableway status, weather, schedule, queue, and update-time data for manual checks or automated alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zopyx](https://clawhub.ai/user/zopyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, operators, and automation builders use this skill to check Table Mountain Aerial Cableway operating status and produce text or JSON reports for manual review or scheduled alerting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs an online status check and may fail or return stale data if the upstream service is unavailable. <br>
Mitigation: Report fetch errors clearly and include the upstream last-updated timestamp in summaries. <br>
Risk: Scheduled or Telegram reporting can create repeated outbound reports if enabled without review. <br>
Mitigation: Confirm schedules, recipients, and reporting behavior before enabling automated alerts. <br>
Risk: Custom URLs or output paths can broaden network or filesystem access beyond the normal status-checking workflow. <br>
Mitigation: Prefer the default status URL and choose output paths explicitly for the intended workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zopyx/table-mountain-status) <br>
- [Table Mountain Aerial Cableway weather API](https://cms.tablemountain.net/admin/actions/submissions/default/weather-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text summaries or JSON, optionally written to a local file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes status, weather, schedule, queue, and last-updated fields when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
