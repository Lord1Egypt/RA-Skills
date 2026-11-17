## Description:

配置赢麻了 API 凭证、浏览官方技能与 Role 目录，或安装/更新其它官方技能与 Role 时使用。请先安装本技能，再由它管理其余条目。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryzhou](https://clawhub.ai/user/jerryzhou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to configure WinMale API credentials, discover official WinMale skills and roles, and install or update the local skill set. It also routes user requests toward installed WinMale skills and roles while preserving credential-handling and output-hygiene rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials and may ask the user to provide WinMale client secrets.

Mitigation: Prefer local environment files or trusted local prompts for credentials, preserve existing credentials during updates, and do not echo full secrets in chat or public files.

Risk: The skill can install or update packages in active agent skill directories.

Mitigation: Install only from trusted WinMale catalog or pack URLs, avoid overridden catalog or base URLs unless intentionally trusted, and review or scan packages before deployment.

Risk: Remote catalog updates can change the available skills, roles, and routing behavior.

Mitigation: Check package metadata and frontmatter after updates, skip deprecated or hidden entries, and verify that role and skill packages are installed through their appropriate paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jerryzhou/skills/wm-skillhub)
- [WinMale Skills Catalog](https://open.winmale.com/api/skills)
- [WinMale SkillHub Install Guide](https://open.winmale.com/install/skillhub.md)
- [WinMale Credentials Page](https://open.winmale.com/skillhub/creds)
- [WinMale Getting Started](https://open.winmale.com/get-started)
- [Errors Recovery Guide](references/errors-recovery.md)
- [Output Hygiene](references/output-hygiene.md)
- [Units and Values](references/units-and-values.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command, configuration, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to preserve local credentials, call WinMale discovery or catalog endpoints, and install or update skill and role packages.]

## Skill Version(s):

1.0.29 (source: frontmatter, manifest.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
