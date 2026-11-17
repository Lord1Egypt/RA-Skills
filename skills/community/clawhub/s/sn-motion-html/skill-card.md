## Description:

Build continuous-shot motion-driven HTML stories from a subject or narrative, including research, story structure, consistent AI stills, Seedance scene and connector clips, interface styling, media normalization, and browser QA. Use for immersive journeys, timelines, product stories, fictional worlds, or other scene-based visual narratives whose camera should flow from beginning to end; not for ordinary autoplay video pages or general web apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to plan and build reusable, scroll-driven visual stories with AI-generated stills, connected video scenes, and a custom web interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key could be sent to an unchecked server address.

Mitigation: Require a verified HTTPS API destination and prevent credentials from following redirects to another origin.

Risk: Running an unfamiliar project configuration with an inherited API key could expose credentials.

Mitigation: Use a dedicated API key with spending limits, and keep project .env files out of hosting and version control.

Risk: Video uploads and retries can incur provider costs.

Mitigation: Approve uploads and retry costs before generation.

Risk: The project template is missing its .env.example file, which may complicate safe setup.

Mitigation: Restore .env.example before initialization and verify that static hosting cannot expose .env.

## Reference(s):

- [Production workflow](artifact/references/workflow.md)
- [Prompting patterns](artifact/references/prompting.md)
- [Motion frontend](artifact/references/frontend.md)
- [Seedance API documentation (Volcengine)](https://www.volcengine.com/docs/82379/1520757?lang=zh)
- [Seedance API reference (Volcengine)](https://www.volcengine.com/docs/82379/1521309?lang=zh)
- [ClawHub release page](https://clawhub.ai/sensenova-skills/skills/sn-motion-html)

## Skill Output:

**Output Type(s):** [Code, HTML, CSS, JavaScript, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Project files, structured content and manifests, prompts, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reusable motion-story project with scenes linked into a scroll-driven continuous camera journey]

## Skill Version(s):

2026.10.29 (source: server-resolved release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
