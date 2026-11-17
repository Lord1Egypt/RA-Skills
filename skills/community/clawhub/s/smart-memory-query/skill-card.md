## Description:

Enforces proactive, query-optimized memory_search usage when prior context is referenced, a new task starts, or a proper noun appears.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jo-minjun](https://clawhub.ai/user/jo-minjun)

### License/Terms of Use:


## Use Case:

Agent users and developers use this skill to make agents retrieve relevant persistent memory before beginning new work or responding to references involving previous decisions, projects, services, tools, or people.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause agents to search persistent memory on most tasks and when names, services, tools, or projects are mentioned.

Mitigation: Install only when broad proactive memory recall is acceptable; for sensitive or compartmentalized work, prefer a narrower memory skill that searches only when prior context is explicitly relevant or requested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jo-minjun/skills/smart-memory-query)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown instructions with inline memory_search query examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to issue short 2-4 token memory_search queries before or during task handling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
