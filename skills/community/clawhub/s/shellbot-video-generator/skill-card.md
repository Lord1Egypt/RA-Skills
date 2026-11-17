## Description:

Video Generator guides agents through creating polished Remotion motion graphics videos, including product promos, demos, short films, and social clips, with Firecrawl-based brand scraping when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cohnen](https://clawhub.ai/user/cohnen)

### License/Terms of Use:


## Use Case:

Developers and content creators use this skill to scaffold Remotion video projects, collect brand assets, compose animated scenes, preview work in Remotion Studio, and render final videos when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Remotion previews may be exposed through a public tunnel.

Mitigation: Require manual approval before opening a tunnel, avoid sensitive preview content, and stop the tunnel when review is complete.

Risk: The workflow can scrape public websites and download remote assets.

Mitigation: Scrape only approved public URLs and review downloaded assets for relevance, safety, and usage rights before including them in a project.

Risk: The skill runs npm and npx commands while scaffolding, previewing, and rendering projects.

Mitigation: Run generated projects in an isolated working directory and review dependency changes before execution in sensitive environments.

Risk: Environment files may be loaded to obtain FIRECRAWL_API_KEY.

Mitigation: Avoid using the skill in directories with untrusted .env files and scope credentials to the minimum access needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cohnen/skills/shellbot-video-generator)
- [Shell homepage](https://getshell.ai)
- [Reusable Components](references/components.md)
- [Remotion Composition Patterns](references/composition-patterns.md)
- [Remotion configuration documentation](https://remotion.dev/docs/config)
- [Firecrawl scrape API](https://api.firecrawl.dev/v1/scrape)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash and TypeScript/TSX code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Remotion project files and downloaded visual assets; Firecrawl scraping requires FIRECRAWL_API_KEY.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
