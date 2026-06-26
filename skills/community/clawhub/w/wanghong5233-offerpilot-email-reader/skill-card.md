## Description: <br>
Classify hiring emails and sync job status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghong5233](https://clawhub.ai/user/wanghong5233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to classify hiring-related emails, sync related job status, review recent classification history, fetch unread mailbox items, and control local heartbeat checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process unread mailbox contents through a local OfferPilot/email backend. <br>
Mitigation: Install only after confirming which mailbox is read, what content is stored, who can access it, and how stored history can be deleted. <br>
Risk: Heartbeat and cron actions can create recurring email checks through the local backend. <br>
Mitigation: Confirm how to start, stop, and audit recurring checks before enabling heartbeat or cron workflows. <br>
Risk: Classification confidence may be low or email type may be irrelevant. <br>
Mitigation: Surface uncertainty clearly and avoid treating low-confidence classifications as authoritative status updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanghong5233/wanghong5233-offerpilot-email-reader) <br>
- [Publisher profile](https://clawhub.ai/user/wanghong5233) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown summaries with inline curl command examples and API response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize fetched and processed email counts, classifications, related jobs, heartbeat status, and API errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
