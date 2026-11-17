## Description:

Soft blocklist guard for OpenClaw that injects a security directive at agent bootstrap and warns on incoming messages referencing blocked terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rgr4y](https://clawhub.ai/user/rgr4y)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to add a soft, configurable blocklist layer to OpenClaw agents that discourages blocked tool, skill, or plugin use and warns when incoming messages mention configured terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies every agent bootstrap context and may suppress discussion, recommendations, installs, or tool use for configured terms.

Mitigation: Install it only when an agent-wide soft blocklist is intended, and review the configured terms before deployment.

Risk: The SNITCH_BLOCKLIST environment variable controls the blocked terms used by the hooks.

Mitigation: Treat SNITCH_BLOCKLIST as trusted configuration and avoid special characters or multiline values.

Risk: The skill documentation references a separate plugin install path for hard enforcement.

Mitigation: Review the separate plugin package before using the unpinned hard-enforcement install command.

Risk: The artifact claims its directive cannot be overridden by user messages or system prompts, while server security evidence says it overstates its authority over system prompts.

Mitigation: Treat the blocklist as soft enforcement and do not rely on it as the only control for high-risk tool blocking.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rgr4y/skills/superpack-snitch)
- [README linked from skill artifact](https://github.com/rgr4y/superpack-snitch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown policy directive and warning text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads SNITCH_BLOCKLIST as a comma-separated environment variable and otherwise uses the default blocked terms.]

## Skill Version(s):

0.0.8 (source: server release evidence; artifact frontmatter reports 0.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
