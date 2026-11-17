## Description:

Classify hiring emails and sync job status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghong5233](https://clawhub.ai/user/wanghong5233)

### License/Terms of Use:

MIT-0

## Use Case:

External users or job seekers use this skill to classify hiring-related email, summarize recent classification history, fetch unread mailbox items for classification, and synchronize related job application status through a trusted local OfferPilot backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process unread email through a local backend.

Mitigation: Install only when the local service on port 8010 is trusted and its mailbox permissions and retention policy are understood.

Risk: The skill can start or stop scheduled email heartbeat checks.

Mitigation: Confirm how scheduled checks are enabled, monitored, and stopped before using heartbeat scheduler commands.

Risk: Email classification can be uncertain for low-confidence or irrelevant messages.

Mitigation: Clearly surface uncertainty and avoid treating low-confidence classifications as final job-status updates without review.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with inline shell commands and API response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report classification confidence, company, interview time, related job ID, updated job status, fetch counts, processing counts, and scheduler or notification status.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
