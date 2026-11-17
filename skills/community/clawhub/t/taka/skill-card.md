## Description:

Taka creative tools CLI -- generate AI images, videos, emails, and flyers for small businesses from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielokaninm](https://clawhub.ai/user/danielokaninm)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and AI agents use this skill to install and operate the Taka CLI for creating and managing marketing creatives such as Instagram posts, email campaigns, flyers, logos, blog content, images, and videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external CLI package that may be installed without a pinned reviewed version.

Mitigation: Install only a reviewed taka-cli version and avoid npx for login or other authenticated actions.

Risk: Authentication stores local access and refresh tokens for the Taka service.

Mitigation: Use a limited Taka account where possible, verify local credential permissions, and log out when the agent no longer needs access.

Risk: Creative management commands can update or delete business creative content.

Mitigation: Review target creative IDs and command arguments before running update, rename, or delete commands.

Risk: The TAKA_SERVER_URL setting can redirect authentication and API traffic to a custom endpoint.

Mitigation: Confirm TAKA_SERVER_URL before authenticating and prefer the documented production endpoint unless staging or self-hosted use is intentional.

## Reference(s):

- [ClawHub Taka Skill Page](https://clawhub.ai/danielokaninm/skills/taka)
- [Taka Website](https://taka.ai)
- [taka-cli npm Package](https://www.npmjs.com/package/taka-cli)
- [README.md](README.md)
- [HOW_TO_RUN.md](HOW_TO_RUN.md)
- [examples/EXAMPLES.md](examples/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON-oriented CLI outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent through Taka CLI commands that install taka-cli, authenticate to Taka, create or update creative projects, and parse JSON command output.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
