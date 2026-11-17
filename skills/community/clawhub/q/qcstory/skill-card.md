## Description:

A Chinese-language QCstory improvement coach that guides users through the nine-step QCstory process, reviews each response against completion standards, and produces a complete improvement report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cocokkxy](https://clawhub.ai/user/cocokkxy)

### License/Terms of Use:

MIT

## Use Case:

Employees, team leads, and continuous-improvement facilitators use this skill to structure a QCstory improvement activity from topic clarification through follow-up. The skill is best suited for Chinese-language coaching where each step needs clear acceptance criteria and a final formatted report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate for broad work-improvement requests and may steer the conversation into a rigid nine-step QCstory process.

Mitigation: Confirm that the user wants QCstory-style coaching before continuing when the request is general or ambiguous.

Risk: Users may include confidential business process details while describing improvement topics, current state, goals, causes, and countermeasures.

Mitigation: Ask users to omit or generalize sensitive operational, customer, financial, or personnel details before sharing examples with the agent.

Risk: The generated improvement report may be incomplete or misleading if the user's inputs are inaccurate, underspecified, or outside the QCstory method.

Mitigation: Have a responsible reviewer check the final report and underlying data before using it for business decisions or implementation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cocokkxy/skills/qcstory)
- [Publisher profile](https://clawhub.ai/user/cocokkxy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese conversational guidance with structured Markdown-style prompts and a final formatted improvement report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent advances one QCstory step at a time, asks for revisions when acceptance criteria are not met, and summarizes the completed activity after all nine steps.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
