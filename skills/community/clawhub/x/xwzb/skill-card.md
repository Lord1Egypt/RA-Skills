## Description: <br>
新闻早报 fetches the latest hotspot/news items from hotspot.api4claw.com, ranks top items by model-estimated reader interest, summarizes them, and groups titles by source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xltang](https://clawhub.ai/user/xltang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers and agents use this skill to produce a current Chinese hotspot briefing, view a ranked Top list with brief summaries, check service status, or group titles by source_name. Optional scheduled delivery is offered only after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requests to hotspot.api4claw.com when invoked. <br>
Mitigation: Install only if that external request is acceptable; the skill should use only the latest-hotspots endpoint disclosed in the release. <br>
Risk: Optional scheduling can create recurring messages to a selected channel or user. <br>
Mitigation: Review the generated cron command before running it, including recipient, channel, and Asia/Shanghai timezone; scheduling requires explicit user approval. <br>
Risk: Live API failures or malformed responses can produce missing or partial briefings. <br>
Mitigation: Report the explicit failure or degraded status, skip malformed items safely, and do not use cached or fabricated content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xltang/xwzb) <br>
- [Hotspot API Endpoint](https://hotspot.api4claw.com/hotspots/latest?timestamp=$TIME_STEMP) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing with optional bash cron command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches live JSON, ranks up to 10 items, omits raw hotness and stored date metadata, and reports failures without fabricating content.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
