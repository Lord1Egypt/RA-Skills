## Description: <br>
Creates Remotion-based animated video projects, templates, and renders when a user explicitly asks an agent to build or edit motion graphics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratyushchauhan](https://clawhub.ai/user/pratyushchauhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to scaffold Remotion projects, customize animation templates, preview compositions, and render videos such as intros, explainers, data clips, and conversation videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scaffold local Node.js projects, run npm and Remotion commands, and write rendered video files in the workspace. <br>
Mitigation: Install and run it only when those local project, command execution, and file output behaviors are intended for the workspace. <br>
Risk: Recurring renders are persistent automation that can continue consuming compute and producing files. <br>
Mitigation: Approve recurring renders only after confirming the exact schedule, output directory, retention or deletion policy, and removal method. <br>
Risk: Generated video content may need review for accuracy, branding, timing, and accessibility before publication. <br>
Mitigation: Preview the Remotion composition and inspect rendered outputs before sharing or deploying them. <br>


## Reference(s): <br>
- [Proactivity Guide](references/proactivity.md) <br>
- [Component Library API](references/component-api.md) <br>
- [Animation Patterns](references/animation-patterns.md) <br>
- [Showcase Video](https://github.com/PratyushChauhan/PratyushChauhan/releases/download/remotion-showcase-v1/remotion-showcase-agent.mp4) <br>
- [ClawHub Skill Page](https://clawhub.ai/pratyushchauhan/remotion-animator) <br>
- [Publisher Profile](https://clawhub.ai/user/pratyushchauhan) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus generated TypeScript, CSS, JSON, and video output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local Remotion project files and can render MP4, ProRes, or WebM video outputs through npm and Remotion commands.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
