## Description:

Searches past conversation history when an agent needs prior decisions, implementation context, unfamiliar workflow guidance, or help after getting stuck.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumoezhung](https://clawhub.ai/user/yumoezhung)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to consult prior conversation history before repeating investigations, choosing an implementation approach, or handling unfamiliar workflows. It is intended to return concise, actionable historical context with sources after the current task is understood.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search and read sensitive archived conversation history too broadly, including past sessions that may contain credentials, private code, or sensitive tool output.

Mitigation: Use explicit prompts, current-project limits, snippet-first reads, and caution around archives likely to contain sensitive material.

## Reference(s):

- [Episodic Memory MCP Tools Reference](artifact/MCP-TOOLS.md)
- [ClawHub Skill Page](https://clawhub.ai/yumoezhung/skills/remembering-conversations)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown synthesis with source references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When used as directed, the search agent summarizes selected conversation results in roughly 200-1000 words.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
