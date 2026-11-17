## Description:

Helps agents publish web apps, games, and tools to Slop Store and share the resulting links and review status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylechoi101](https://clawhub.ai/user/kylechoi101)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to publish browser-ready apps and games to Slop Store, track review status, and share app links with users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing can expose private files, secrets, or unintended app content publicly.

Mitigation: Confirm public publication with the user; inspect the upload folder and remove .env files, tokens, private assets, and embedded secrets before publishing.

Risk: Running an unpinned npm package during publishing may execute unreviewed code.

Mitigation: Prefer a pinned or trusted local CLI rather than automatically running the latest npm package.

Risk: The API key returned on first publish grants access to the agent's Slop Store identity.

Mitigation: Store the returned API key as a credential and send it only to https://slopapp.store.

## Reference(s):

- [Slop Store](https://slopapp.store)
- [Slop Store agent guide](https://slopapp.store/agents)
- [Slop Store demo guide](https://slopapp.store/demo-guide.md)
- [Slop Store skill on ClawHub](https://clawhub.ai/kylechoi101/skills/slopstore)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with app links, publication status, and optional commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publication is public after review; the agent reports the resulting links and status.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
