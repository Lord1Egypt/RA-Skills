## Description:

Adaptive skill scheduling engine with environment-aware routing, user preferences, and self-learning optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[namechenxinyu](https://clawhub.ai/user/namechenxinyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Skill Pilot to route tasks across installed skills, choose default or full comparison mode, adapt routing to local network conditions and preferences, and generate observability reports about skill performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoked tools and child processes may inherit broad local environment access.

Mitigation: Run the skill in a restricted environment with only the minimum environment variables needed for the selected downstream tools.

Risk: Execution history, reports, queries, URLs, errors, and context may be stored in plaintext.

Mitigation: Treat Skill Pilot history and report files as sensitive local data and avoid placing secrets in prompts, URLs, or the skill directory.

Risk: The scheduler can execute other local skills and CLIs.

Mitigation: Install and enable it only in environments where executing local skills and CLIs through the scheduler is acceptable.

## Reference(s):

- [Skill Pilot ClawHub Page](https://clawhub.ai/namechenxinyu/skills/skill-pilot)
- [Capability Taxonomy](references/capability-taxonomy.md)
- [Micro Routing Examples](references/micro-routing-examples.md)
- [Reminder Policy](references/reminder-policy.md)
- [Resolution Order](references/resolution-order.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text reports with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected tool names, sources, comparison reports, performance metrics, and routing recommendations.]

## Skill Version(s):

0.4.6 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
