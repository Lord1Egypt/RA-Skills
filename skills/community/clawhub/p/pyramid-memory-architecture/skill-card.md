## Description:

Pyramid Memory Architecture is an agent skill for organizing AI-agent memory into layered files, guiding rule placement, redundancy checks, cron trigger design, and workspace initialization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[popo67ll](https://clawhub.ai/user/popo67ll)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to initialize and maintain AI-agent workspaces with clear memory layers for rules, personality, heartbeat tasks, local tool notes, and technical implementation details. It also helps agents audit markdown memory files for redundancy, misplaced rules, broken anchors, and cron payload design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to inspect private memory, user-profile, tool, cookie, API-key, or repository information.

Mitigation: Use explicit file allowlists and exclude credential-bearing or private paths unless the user has authorized that access for the task.

Risk: Recurring cron workflows can cause repeated scans or actions that the user did not intend.

Mitigation: Keep cron workflows disabled unless they are deliberately configured, reviewed, and scoped.

Risk: Cleanup or GitHub synchronization guidance could alter or publish workspace content.

Mitigation: Require separate confirmation before cleanup, file deletion, commits, tags, or GitHub pushes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/popo67ll/skills/pyramid-memory-architecture)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Markdown guidance with file templates, checklists, JSON payload examples, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose workspace file edits, cron payloads, redundancy-check reports, and memory-layer classification decisions.]

## Skill Version(s):

3.6.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
