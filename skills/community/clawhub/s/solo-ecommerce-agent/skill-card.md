## Description: <br>
Automates multi-platform e-commerce operations including product discovery, listing preparation, customer-service replies, order handling, and daily reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hnc87](https://clawhub.ai/user/hnc87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators and developers use this skill to configure an agent that scans product opportunities, prepares listings, drafts customer replies, processes order records, and summarizes store activity across platforms such as Douyin, Taobao, Pinduoduo, and JD. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be configured for unattended publishing, customer replies, shipping, refunds, and order handling in live stores. <br>
Mitigation: Start with a test store or narrowly permissioned account, and keep publishing, shipping, refunds, and customer replies behind human approval until safeguards are verified. <br>
Risk: The skill stores customer, order, product, recommendation, and operational log data on the local filesystem. <br>
Mitigation: Protect the data directory, limit access to credentials and customer records, and regularly delete or rotate local operational data that is no longer needed. <br>
Risk: Frequent cron execution can repeatedly act on store backends without sufficient review. <br>
Mitigation: Avoid unattended cron schedules in production until each module has been tested, platform permissions are scoped, and exception handling or manual escalation is in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hnc87/solo-ecommerce-agent) <br>
- [Platform operation guide](artifact/references/platform_guides.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code, markdown] <br>
**Output Format:** [Markdown instructions, JSON configuration, Python scripts, shell commands, and generated text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local JSON records and daily log/report files under the configured e-commerce data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
