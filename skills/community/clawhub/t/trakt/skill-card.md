## Description:

Track and view watched movies and TV shows via Trakt.tv, including watch history and movie or show search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjrussell](https://clawhub.ai/user/mjrussell)

### License/Terms of Use:


## Use Case:

External users use this skill to have an agent query Trakt.tv watch history and search for movies or TV shows. History lookups require Trakt authentication, while search can be used without authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the required trakt-cli package globally with npm can execute third-party package code.

Mitigation: Install only if you trust the trakt-cli npm package, avoid elevated privileges, and review the package before deployment.

Risk: Trakt OAuth setup uses a client secret and stores credentials in ~/.trakt.yaml.

Mitigation: Use a safer secret-entry method if the CLI supports one and confirm ~/.trakt.yaml is readable only by the current user.

Risk: Watch history commands access personal viewing history after authentication.

Mitigation: Use the skill only with accounts whose watch history the user is authorized to access.

## Reference(s):

- [Trakt](https://trakt.tv)
- [Trakt OAuth Applications](https://trakt.tv/oauth/applications/new)
- [ClawHub Trakt Skill](https://clawhub.ai/mjrussell/skills/trakt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only Trakt.tv history and search command guidance; history access depends on local authentication.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
