## Description:

Helps create faceless tutorial video kits by drafting a marked script, recording brief, visual asset plan, manifest, and packaged AI or web resources for editing outside the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to turn a tutorial idea or script into a faceless short-form video kit with a script, recording brief, visual assets, and an edit manifest. The final video is assembled by the creator in CapCut or another editor unless they intentionally run the optional local render path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes local render, Homebrew, bootstrap, and privileged npm troubleshooting commands.

Mitigation: Review and run those commands manually only when local environment changes are intended.

Risk: The artifact contains conflicting behavior around kit-only delivery versus optional local video rendering.

Mitigation: Use the kit-generation path by default, and invoke /tutorial-render only after confirming that local rendering is desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/tutorial-viral-f100k)
- [formula100k publisher profile](https://clawhub.ai/user/formula100k)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documents, manifests, shell commands, and packaged asset files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces GUION.md, BRIEF_GRABACION.md, MANIFEST.md, and a structured asset zip; optional local render commands require manual review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
