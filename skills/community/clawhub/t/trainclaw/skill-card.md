## Description:

TrainClaw helps agents query China Railway 12306 for tickets, route stops, and transfer plans with train-type, time-window, and duration filters plus text, JSON, or CSV output.

This skill is for research and development only.

## Publisher:

[ai4mse](https://clawhub.ai/user/ai4mse)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use TrainClaw to look up China rail availability, train stops, and transfer plans from 12306 without account credentials. It is useful when an agent needs to answer rail itinerary questions or return rail data in human-readable or structured formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts 12306 services with the routes and dates requested by the user.

Mitigation: Use the skill only for China rail lookup and avoid submitting route/date queries that should remain private.

Risk: Verbose logs or shared outputs may reveal rail query details.

Mitigation: Avoid sharing verbose logs and review outputs before forwarding them outside the execution environment.

Risk: The release has ordinary dependency hardening gaps.

Mitigation: Install dependencies in an isolated environment and pin the requests dependency when stronger reproducibility is required.

Risk: Broad trigger wording may cause the skill to run for ambiguous travel prompts.

Mitigation: Confirm the user wants a China rail lookup before running commands when the request is ambiguous.

## Reference(s):

- [TrainClaw ClawHub page](https://clawhub.ai/ai4mse/skills/trainclaw)
- [AI4MSE publisher profile](https://clawhub.ai/user/ai4mse)
- [China Railway 12306](https://www.12306.cn/index/)
- [12306 query service](https://kyfw.12306.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and text, JSON, or CSV command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ticket queries can emit text, JSON, or CSV; route and transfer queries can emit text or JSON.]

## Skill Version(s):

0.0.7 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
