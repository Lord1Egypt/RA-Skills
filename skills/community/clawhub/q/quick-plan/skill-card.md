## Description:

Quick Plan turns an implementation discussion into a TDD-driven markdown plan when no finalized spec exists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to convert an ongoing feature discussion into a focused implementation plan when no reviewed spec exists. It reconstructs intent, checks for gaps, explores the codebase through scoped experts where available, and writes a markdown plan after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated implementation plan can preserve incorrect assumptions from the conversation or code exploration.

Mitigation: Review the draft plan before approving the final plan path, paying attention to assumptions, file references, and test commands.

Risk: The skill reads the current conversation and relevant project files to reconstruct intent.

Mitigation: Use it only in workspaces where that context is appropriate for the planning agent to read.

## Reference(s):

- [Quick Plan skill page](https://clawhub.ai/anderskev/skills/quick-plan)
- [Fanout Exploration + Expert Subagent Brief](references/fanout-brief.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown plan with checklists, code or shell command snippets, and concise handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the approved plan to .beagle/plans/<slug>/plan.md; does not execute the plan.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
