## Description:

Dispatch independent tasks to focused agents that work concurrently on isolated problems without shared state or sequential dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demo112](https://clawhub.ai/user/demo112)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to split independent failures, bugs, or subsystem tasks into focused subagent assignments, then review and integrate the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parallel subagents may make conflicting concurrent edits if assigned overlapping files, shared state, or sequentially dependent tasks.

Mitigation: Dispatch only independent scopes, give each agent focused constraints, review returned summaries for conflicts, and run the full relevant test suite before integration.

Risk: Subagent findings can be incomplete or incorrect when prompts omit necessary context or expected output.

Mitigation: Provide self-contained task prompts with concrete failures, constraints, and requested return format, then spot-check the resulting changes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/demo112/skills/superpowers-dispatching-parallel-agents)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown guidance with prompt examples and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces self-contained delegation prompts and integration checklists for the coordinating agent.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
