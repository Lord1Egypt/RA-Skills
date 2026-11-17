## Description:

Website Pickpocket helps agents guide authorized website copying into offline static sites or React, Vue, Angular, Svelte, or Tailwind project outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenyangze](https://clawhub.ai/user/zhenyangze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan authorized website capture, offline browsing, backup migration, and conversion of crawled pages into common frontend project structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used to copy websites without proper authorization.

Mitigation: Use it only for sites the user owns or has explicit permission to copy, and check site terms before crawling or republishing content.

Risk: Session cookies or localStorage examples can place active credentials into plaintext configuration.

Mitigation: Avoid real session tokens in configuration; if credentials are required, store them as protected secrets, limit their scope, and rotate them after use.

Risk: Crawler settings can collect more pages or resources than intended.

Mitigation: Keep depth, page limit, concurrency, and resource-size limits conservative, and write output to a dedicated directory.

Risk: Anti-crawling bypass advice can encourage inappropriate access attempts.

Mitigation: Do not bypass access controls or site protections; stop when authorization, robots guidance, or rate limits are unclear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenyangze/skills/website-pickpocket-skill)
- [Server-Resolved GitHub Source](https://github.com/zhenyangze/website-pickpocket-skill)
- [Publisher Profile](https://clawhub.ai/user/zhenyangze)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, and generated project/file structure descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose crawler limits, framework selections, output directories, and resource-handling options.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
