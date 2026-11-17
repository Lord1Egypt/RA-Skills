## Description:

Xunlei helps agents explain download acceleration mechanics, compare Xunlei cloud and local download workflows, and guide remote download or NAS setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to understand Xunlei download acceleration, assess membership and cloud-storage trade-offs, manage download tasks, and configure remote or NAS-based download workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The NAS Docker example uses host networking, privileged mode, mutable latest image tags, and broad host volume access.

Mitigation: Use a pinned and verified image digest, bridge networking with only required ports, no privileged mode unless specifically justified, a dedicated non-root user, narrowly scoped writable volumes, and firewall or authentication controls for the web interface.

Risk: Download guidance can be misused for copyrighted or unauthorized content.

Mitigation: Follow the skill's stated boundary to use legal resources only and avoid piracy channels, cracked memberships, or bypass methods.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangifonly/skills/xunlei)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Docker and NAS configuration recommendations; users should review commands before execution.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
