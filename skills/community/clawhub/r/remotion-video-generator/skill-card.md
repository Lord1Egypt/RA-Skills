## Description:

AI video production workflow using Remotion. Use when creating videos, short films, commercials, or motion graphics. Triggers on requests to make promotional videos, product demos, social media videos, animated explainers, or any programmatic video content. Produces polished motion graphics, not slideshows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zendenho7](https://clawhub.ai/user/zendenho7)

### License/Terms of Use:


## Use Case:

Developers and content teams use this skill to create programmatic motion graphics videos, including promotional videos, product demos, short films, social media clips, animated explainers, and commercials. It helps agents scaffold Remotion projects, gather brand assets, build scenes, preview work, iterate, and render final video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted URL passed to the scraping helper could trigger code execution due to unsafe input handling.

Mitigation: Review or patch the helper script before use, validate and quote user-supplied URLs, and require explicit approval before running scraping commands.

Risk: The workflow can scrape user-specified websites, download remote assets, and use third-party screenshot services.

Mitigation: Confirm that scraping and asset downloads are authorized for the target site, inspect downloaded assets before use, and avoid third-party screenshot services unless the user approves them.

Risk: The workflow can expose a local Remotion Studio to the public internet through a tunnel.

Mitigation: Use local preview by default and require explicit user approval before starting any public tunnel.

Risk: The workflow installs npm and pip packages without pinned versions.

Mitigation: Pin dependencies, review generated package files, and run installation in an isolated workspace.

## Reference(s):

- [Remotion](https://www.remotion.dev/)
- [Scrapling](https://github.com/D4Vinci/Scrapling)
- [React](https://react.dev/)
- [Superskills - Video Generator (Remotion)](https://superskills.vibecode.run/)
- [Video Components](references/components.md)
- [Composition Patterns](references/composition-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/zendenho7/skills/remotion-video-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, JSON, Python, and TypeScript/TSX code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project files, Remotion source code, package configuration, preview commands, and render commands when used by an agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
