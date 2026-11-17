## Description:

Multi-path reasoning for complex problems that guides an agent to explore, evaluate, prune, backtrack, and select among solution branches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobisamaa](https://clawhub.ai/user/tobisamaa)

### License/Terms of Use:


## Use Case:

Developers, operators, and agents use this skill for complex decisions, creative problems, ambiguous situations, and optimization tasks where comparing multiple approaches is useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local caching or session logs may retain sensitive prompts, problem statements, or decisions.

Mitigation: Disable caching with --no-cache and avoid session logging for confidential business, personal, security, or incident-response prompts.

Risk: Reasoning proposals can be incorrect or misleading when applied to high-cost or ambiguous decisions.

Mitigation: Review generated branches, scores, and selected paths before acting on the recommendation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobisamaa/skills/tree-of-thoughts)
- [ClawHub publisher profile](https://clawhub.ai/user/tobisamaa)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May document reasoning sessions and cache problem statements when those workflows are enabled.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
