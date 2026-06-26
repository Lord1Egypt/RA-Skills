## Description: <br>
AI video production workflow using Remotion. Use when creating videos, short films, commercials, or motion graphics. Triggers on requests to make promotional videos, product demos, social media videos, animated explainers, or any programmatic video content. Produces polished motion graphics, not slideshows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diederik24](https://clawhub.ai/user/diederik24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to plan, scaffold, preview, iterate on, and render Remotion-based motion graphics videos for product demos, promotional clips, explainers, social media videos, and similar programmatic video work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose a local Remotion preview through a public Cloudflare tunnel. <br>
Mitigation: Use it only for non-sensitive projects, require explicit confirmation before starting the tunnel, share only intended preview content, and stop the tunnel and development server when review is finished. <br>
Risk: The workflow uses external brand scraping and remote asset downloads. <br>
Mitigation: Confirm the target URLs before scraping or downloading assets, avoid confidential or private URLs, and use limited Firecrawl credentials. <br>


## Reference(s): <br>
- [Video Generator on ClawHub](https://clawhub.ai/diederik24/skill-5) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Remotion project guidance and may direct creation of local project files, dependency installs, a development server, a public preview tunnel, and an exported MP4 when requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
