## Description: <br>
日程协办虾 helps agents coordinate Feishu meetings by checking availability, creating and managing calendar events, replying to invitations, and preparing meeting context from Feishu documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents with Feishu access use this skill to schedule meetings, find shared availability, manage calendar events, respond to invitations, and prepare meeting background materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform sensitive calendar actions such as creating, changing, deleting, replying to, and inviting attendees to meetings. <br>
Mitigation: Require explicit user confirmation before calendar writes, deletes, RSVP changes, attendee invitations, document searches, or sync subscriptions. <br>
Risk: The fallback script caches a tenant access token in a shared temporary path. <br>
Mitigation: Prefer the OAuth-based openclaw-lark plugin path; avoid the fallback script on shared machines unless the token cache is moved to a private permission-restricted location. <br>
Risk: The fallback app-credential path has weaker user scoping and cannot provide the same personal-calendar behavior as the OAuth plugin path. <br>
Mitigation: Limit app permissions, use the fallback only for app-calendar operations, and direct personal freebusy or invitation-response workflows through the OAuth plugin path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/schedule-sync-claw) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/tujinsama) <br>
- [Feishu Calendar API Reference](references/feishu-calendar-api.md) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional shell command invocations and structured calendar summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu OAuth authorization or app credentials depending on the selected calendar access path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
