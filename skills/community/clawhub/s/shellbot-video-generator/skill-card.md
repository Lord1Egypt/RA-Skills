## Description: <br>
AI video production workflow using Remotion for creating videos, short films, commercials, motion graphics, promotional videos, product demos, social media videos, and animated explainers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cohnen](https://clawhub.ai/user/cohnen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content-producing agents use this skill to scaffold Remotion projects, gather brand assets, compose motion graphics scenes, preview videos, and render final exports when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may scrape target websites and download external brand assets. <br>
Mitigation: Use only approved public URLs, avoid internal or sensitive sites, and review downloaded assets before including them in generated video projects. <br>
Risk: The workflow requires a Firecrawl API key and may read environment files. <br>
Mitigation: Provide only the required API key, keep credentials out of prompts and generated assets, and avoid using the skill in projects that contain unrelated secrets. <br>
Risk: The workflow may expose a local Remotion preview server through a public tunnel. <br>
Mitigation: Require explicit approval before opening a tunnel, share the URL only with intended reviewers, and stop the tunnel immediately after preview. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cohnen/shellbot-video-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/cohnen) <br>
- [Homepage](https://getshell.ai) <br>
- [Reusable Components](references/components.md) <br>
- [Remotion Composition Patterns](references/composition-patterns.md) <br>
- [Remotion Configuration Documentation](https://remotion.dev/docs/config) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline bash commands and generated Remotion project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local video project source files, downloaded visual assets, preview-server instructions, and rendered video files when export is explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
