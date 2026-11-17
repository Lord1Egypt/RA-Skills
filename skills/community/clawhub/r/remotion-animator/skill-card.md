## Description:

Create animated videos programmatically using Remotion from agent-scaffolded projects, reusable templates, and render commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratyushchauhan](https://clawhub.ai/user/pratyushchauhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to scaffold Remotion video projects, customize animation templates for intros, explainers, metrics, and dialogue videos, and render compositions to video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project scaffolding and render helpers can write files outside the intended working area if users provide unsuitable names or output paths.

Mitigation: Use simple relative project names and project-local output paths, then review generated files before rendering.

Risk: Dependency installation and Remotion rendering rely on the Node/npm supply chain.

Mitigation: Review dependencies and consider pinning them with a lockfile before running npm install or render commands.

Risk: Recurring cron renders can persist after setup and repeatedly consume compute or create files.

Mitigation: Enable recurring renders only after explicit confirmation of schedule, output directory, retention policy, and disable method.

## Reference(s):

- [Component Library API](references/component-api.md)
- [Animation Patterns](references/animation-patterns.md)
- [Proactivity Guide for Remotion Animator](references/proactivity.md)
- [Showcase Video](https://github.com/PratyushChauhan/PratyushChauhan/releases/download/remotion-showcase-v1/remotion-showcase-agent.mp4)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets and shell commands; generated project files are TypeScript, CSS, JSON, and video outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project scaffolds and render commands for Remotion compositions; rendered media can include MP4, ProRes, or WebM depending on command options.]

## Skill Version(s):

1.0.7 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
