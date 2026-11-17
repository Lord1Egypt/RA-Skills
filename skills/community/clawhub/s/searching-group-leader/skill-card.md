## Description:

Searching Group Leader breaks search requests into complementary sub-tasks and assigns them to suitable search agents, always including General_Search_Agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urrrich0](https://clawhub.ai/user/urrrich0)

### License/Terms of Use:


## Use Case:

External users and agent builders use this skill to coordinate search workflows that need several complementary search agents. It helps decompose a request into up to eight focused sub-tasks and route date-specific tasks away from Academic_Search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search requests may be delegated to multiple agents, so poorly scoped sub-tasks can produce incomplete or misleading search coverage.

Mitigation: Review generated sub-task descriptions and agent assignments before relying on the combined search results.

Risk: The skill always includes General_Search_Agent and avoids Academic_Search for date-specific tasks, which may be inappropriate for some specialized research workflows.

Mitigation: Confirm the delegated agents match the user's query type and add manual specialist review when academic sources are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urrrich0/skills/searching-group-leader)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text or Markdown task delegation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include up to eight sub-task assignments and runtime date substitution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
