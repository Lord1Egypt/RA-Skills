## Description:

ReelOnce orchestrates an end-to-end text-to-video workflow from story planning through asset images, storyboard images, TTS, shot video generation, Remotion project generation, and final MP4 rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pampas-lab](https://clawhub.ai/user/pampas-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to turn a story prompt or input file into ReelOnce project assets, a Remotion project, and an optional final MP4 video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running the skill can execute project Python and npm dependencies.

Mitigation: Install it only in trusted repositories and virtual environments, and review Python and npm dependency manifests before rendering.

Risk: Text prompts, images, audio, or reference media may be sent to configured media-generation providers.

Mitigation: Use only approved providers for the data involved, avoid sensitive inputs, and use no-render or no-upload style options when limiting rendering or provider transmission.

Risk: Final video rendering can run npm install inside the generated Remotion project.

Mitigation: Review the generated Remotion project and dependencies before rendering, or use --no-render when only project generation is needed.

## Reference(s):

- [ReelOnce skill reference](references/README.md)
- [skills.video provider setup](https://skills.video/)
- [ClawHub skill page](https://clawhub.ai/pampas-lab/skills/reelonce)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, json, files]

**Output Format:** [Markdown guidance with optional JSON results and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes ReelOnce project outputs under output/{project_id}/, including narration.json, assets.json, pipeline-result.json, a project database, a Remotion React project, and optionally a final MP4.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
