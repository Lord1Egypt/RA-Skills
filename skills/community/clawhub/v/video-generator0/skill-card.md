## Description:

Creates professional motion graphics videos using React and Remotion for commercials, demos, social media, and programmatic video content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahqazi-dev](https://clawhub.ai/user/ahqazi-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scaffold and operate Remotion video projects for product demos, commercials, social media clips, short films, and other programmatic video content. It can scrape public brand information with Firecrawl when a product or company URL is provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a local Remotion development server publicly through a Cloudflare tunnel.

Mitigation: Require explicit user approval before opening any tunnel, and use authentication, short-lived access, or other access controls for shared preview URLs.

Risk: The skill runs mutable npm tooling such as create-video and remotion commands.

Mitigation: Pin package versions, prefer locked local dependencies, and review generated project changes before execution or deployment.

Risk: Firecrawl scraping can send supplied URLs and page data to an external service.

Mitigation: Use Firecrawl only with public URLs and do not submit private, internal, confidential, or access-controlled pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahqazi-dev/skills/video-generator0)
- [Firecrawl scrape API endpoint](https://api.firecrawl.dev/v1/scrape)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and generated React/Remotion project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create files under output/<project-name>/ and render video only when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill declaration)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
