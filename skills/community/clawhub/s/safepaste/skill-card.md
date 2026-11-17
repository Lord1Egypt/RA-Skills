## Description:

Check any OpenClaw prompt, config snippet, or tip against the user's actual setup before applying it, with compatibility analysis, exact modifications, backups, and rollback support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rocanome](https://clawhub.ai/user/rocanome)

### License/Terms of Use:


## Use Case:

External OpenClaw users and developers use this skill to review prompts, configuration snippets, skill recommendations, model-routing changes, and workflow tips against their current local setup before deciding whether to apply them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to read broad local OpenClaw workspace, memory, identity, security, tool, model/config, and project context.

Mitigation: Install only if that local context access is acceptable for your environment, and avoid using the skill in workspaces containing secrets or sensitive material that the agent should not inspect.

Risk: Apply and rollback flows can change local OpenClaw configuration and may not cover every possible failure or partial-change scenario.

Mitigation: Review the exact diff before applying changes, confirm that a fresh backup exists, and verify the workspace after any rollback.

Risk: The skill maintains local usage state and may occasionally include Claw Mentor promotional messaging.

Mitigation: Review or disable the tracking and upsell behavior if persistent local state or promotional output is not acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rocanome/skills/safepaste)
- [SafePaste Homepage](https://clawmentor.ai/safepaste)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with optional diffs, code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose exact changes, create local backups before applying changes, and provide rollback guidance.]

## Skill Version(s):

2.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
