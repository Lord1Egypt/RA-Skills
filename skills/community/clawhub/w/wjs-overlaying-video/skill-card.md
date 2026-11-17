## Description:

Adds post-production overlays to existing video clips, including AI-generated cover frames, HTML/CSS captions synced to SRT, kinetic illustrations, chapter chips, end-card CTAs, and HyperFrames render scaffolding for upload-ready MP4s.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianshuo](https://clawhub.ai/user/jianshuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video production agents use this skill to turn segmented or finished clips into composed HyperFrames projects with captions, covers, motion graphics, and render commands. It is oriented toward WJS/Wang Jianshuo Chinese video production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can force fixed WJS/Wang Jianshuo CTA branding into rendered video outputs.

Mitigation: Review the generated cover, CTA, and overlay text before rendering or publication, and remove or replace branding when it is not intended.

Risk: Untrusted spec.json files or custom overlay fragments can influence generated HTML, CSS, JavaScript, file paths, and render behavior.

Mitigation: Use only trusted specs and fragments, inspect custom overlay content before scaffolding, and avoid processing untrusted project inputs.

Risk: The workflow invokes local tools and package execution during scaffolding and rendering.

Mitigation: Run rendering in a sandbox with limited filesystem and network access, pinned dependencies, and manual review before using destructive options such as --force.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jianshuo/skills/wjs-overlaying-video)
- [SKILL.md](artifact/SKILL.md)
- [build_hf_clips.py](artifact/references/build_hf_clips.py)
- [custom_overlay_recipes.md](artifact/references/custom_overlay_recipes.md)
- [example_spec.json](artifact/references/example_spec.json)
- [illustration_patterns.md](artifact/references/illustration_patterns.md)
- [illustrations.py](artifact/references/illustrations.py)
- [scaffold.py](artifact/scripts/scaffold.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON specs, Python scaffolding, HTML/CSS/JavaScript snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to create HyperFrames project files and render workflows for final MP4 production.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
