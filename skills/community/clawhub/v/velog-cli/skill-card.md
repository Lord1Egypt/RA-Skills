## Description:

Fetch and display the latest Velog user posts from public RSS feeds in Markdown or JSON without requiring authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workflow maintainers use this skill to fetch a Velog user's latest public posts for newsletters, digests, or agent context without authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI makes outbound HTTPS requests to Velog for supplied usernames, which may disclose lookup targets to Velog and depends on Velog availability.

Mitigation: Install and run it only where public Velog lookups are acceptable, and apply reviewed network policy in controlled environments.

Risk: The artifact declares an unpinned requests dependency, which can reduce reproducibility across installations.

Mitigation: Use pinned dependency versions or a reviewed lockfile for managed deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chloepark85/skills/velog-cli)
- [Velog Official Site](https://velog.io)
- [Velog Public RSS Feed Pattern](https://v2.velog.io/rss/{username})

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown bullet lists or JSON arrays returned by a command-line workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The username, limit, and output format control which public posts are fetched and how they are displayed.]

## Skill Version(s):

0.1.0 (source: server release metadata, SKILL.md frontmatter, pyproject.toml, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
