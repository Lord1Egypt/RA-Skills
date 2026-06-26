## Description: <br>
AI video production workflow using Remotion for creating polished motion graphics videos, short films, commercials, product demos, social media videos, and animated explainers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zendenho7](https://clawhub.ai/user/zendenho7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative agents use this skill to plan, scaffold, preview, iterate on, and render Remotion-based motion graphics videos such as promotional videos, product demos, social media clips, commercials, and animated explainers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose a local Remotion Studio through a public Cloudflare tunnel. <br>
Mitigation: Use the tunnel only when public preview access is intended, share the URL selectively, and stop the tunnel and dev server when preview work is finished. <br>
Risk: The scraping helper should not be used with private, internal, sensitive, or unusual URLs. <br>
Mitigation: Use only public, non-sensitive brand URLs for scraping and review extracted content before reusing it in generated video projects. <br>
Risk: The server security review reports that the scraping helper can run unsafe input as code. <br>
Mitigation: Review the script before installation or execution, avoid untrusted URL inputs, and run it in a constrained workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zendenho7/remotion-video-generator) <br>
- [Superskills - Video Generator (Remotion)](https://superskills.vibecode.run/) <br>
- [Remotion documentation](https://www.remotion.dev/) <br>
- [Scrapling](https://github.com/D4Vinci/Scrapling) <br>
- [React documentation](https://react.dev/) <br>
- [Video Components](references/components.md) <br>
- [Composition Patterns](references/composition-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript, JSON, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Remotion project files and final video artifacts when executed by an agent with the required local tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
