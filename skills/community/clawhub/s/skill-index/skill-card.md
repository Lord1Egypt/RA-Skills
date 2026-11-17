## Description:

Multi-platform skill ranking and discovery system with 25,000+ skills, supporting Tencent SkillHub, Xfyun SkillHub, and local skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runze123](https://clawhub.ai/user/runze123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover, rank, search, inspect, and optionally install agent skills from remote catalogs and local installations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install third-party skills based on remote catalog data with limited provenance.

Mitigation: Use dry-run first, verify the skill name and publisher outside the ranking output, and avoid non-dry-run installs for untrusted catalog entries.

Risk: Remote catalog data and the local ranking database may be stale or unverified.

Mitigation: Treat rankings as recommendation data rather than a security signal, and confirm important metadata against trusted sources before installing.

Risk: Custom API endpoints can change the trust boundary for catalog data.

Mitigation: Use custom API endpoints only when the endpoint operator and returned data are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runze123/skills/skill-index)
- [Skill Rank Architecture](references/architecture.md)
- [Tencent SkillHub](https://skillhub.tencent.com)
- [Xfyun SkillHub](https://skill.xfyun.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI commands and ranked text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use network data, a local SQLite cache, and dry-run installation previews.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
