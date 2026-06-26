## Description: <br>
Monitor available TestFlight beta slots with smart app lookups and silent batch checking. Get alerted when slots open up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jon-xo](https://clawhub.ai/user/jon-xo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to monitor one or more Apple TestFlight beta links, resolve app names from TestFlight codes, and receive alerts when previously full betas appear to have open seats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged batch configuration includes an example TestFlight URL that may be checked if left in place. <br>
Mitigation: Review config/batch-config.json before installation and remove or replace the example link with URLs you intend to monitor. <br>
Risk: Monitoring makes outbound requests to Apple TestFlight links and stores monitored URLs locally. <br>
Mitigation: Add only TestFlight URLs you are comfortable checking from this environment and retaining in local configuration or state files. <br>
Risk: The cron example creates ongoing scheduled checks. <br>
Mitigation: Disable or remove the cron job when monitoring is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jon-xo/testflight-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/jon-xo) <br>
- [awesome-testflight-link Lookup Data](https://github.com/pluwen/awesome-testflight-link) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Terminal text and Markdown-style alert messages, with JSON configuration and state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch mode is designed to stay silent unless monitored TestFlight availability changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
