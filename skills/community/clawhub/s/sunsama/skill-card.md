## Description: <br>
Sunsama MCP integration with managed authentication for managing daily tasks, calendar events, backlog, objectives, time tracking, and linked email threads from connected Gmail or Outlook accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage Sunsama planning workflows, including tasks, backlog items, calendar scheduling, objectives, timers, and connected email threads through Maton-managed authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and OAuth connection to mediate access to Sunsama and linked Gmail or Outlook email threads. <br>
Mitigation: Install only when Maton-mediated Sunsama and email access is intended, keep MATON_API_KEY private, and rotate or revoke the key if exposure is suspected. <br>
Risk: Write, delete, meeting, calendar, recurring-task, and email-thread actions can modify or remove user data. <br>
Mitigation: Review the target resource and intended effect before approving each write, delete, meeting, calendar, recurring-task, or email operation. <br>


## Reference(s): <br>
- [Sunsama ClawHub release](https://clawhub.ai/byungkyu/sunsama) <br>
- [Publisher profile](https://clawhub.ai/user/byungkyu) <br>
- [Maton homepage](https://maton.ai) <br>
- [Sunsama](https://sunsama.com) <br>
- [Maton community](https://discord.com/invite/dBfFAcefs2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON schemas and example Python, JavaScript, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized Sunsama MCP connection.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
