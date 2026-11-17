## Description:

Discover and install related skills from the inference.sh skill registry to find complementary capabilities for AI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to discover, install, update, and combine complementary skills from the inference.sh registry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can suggest broad skill-management commands that persistently change the agent setup.

Mitigation: Review each add, update, or remove command before execution and avoid bulk installs unless the resulting skill versions and permissions have been checked.

Risk: Install and update commands are not pinned to reviewed versions.

Mitigation: Prefer pinned or explicitly reviewed skill versions and trust the skills CLI, registry, and selected skills before applying changes.

## Reference(s):

- [Agent Skills Overview](https://inference.sh/blog/skills/skills-overview)
- [Getting Started](https://inference.sh/docs/getting-started/introduction)
- [Apps Overview](https://inference.sh/docs/apps/overview)
- [CLI Setup](https://inference.sh/docs/extend/cli-setup)
- [What is inference.sh?](https://inference.sh/docs/getting-started/what-is-inference)
- [inference.sh Explore](https://inference.sh/explore)
- [ClawHub skill page](https://clawhub.ai/okaris/skills/related-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill-management commands that persistently change the agent environment.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
