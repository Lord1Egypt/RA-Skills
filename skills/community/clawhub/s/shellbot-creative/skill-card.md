## Description:

Shellbot Creative helps agents plan and orchestrate creative production workflows for image and video generation, image editing, motion scenes, voiceovers, music, and Remotion assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cohnen](https://clawhub.ai/user/cohnen)

### License/Terms of Use:


## Use Case:

Developers, creators, and marketing teams use this skill to turn a brief into storyboards, provider routing, generated asset plans, audio steps, and Remotion-ready assembly guidance for explainers, product marketing videos, social ads, and reusable creative asset pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated shell plans may execute unsafe commands if a brief or prompt is crafted maliciously.

Mitigation: Review generated shell plans before running them, especially when the brief came from another person or an untrusted source.

Risk: Prompts and media may be sent to external creative providers.

Mitigation: Do not include secrets, unreleased campaign details, customer data, or private media unless sharing them with the selected provider is acceptable.

Risk: The Remotion setup path may use npx create-video@latest, which can change over time.

Mitigation: Pin or avoid npx create-video@latest in controlled environments.

## Reference(s):

- [Creative Guidelines](references/creative-guidelines.md)
- [Provider Matrix](references/provider-matrix.md)
- [Remotion Playbook](references/remotion-playbook.md)
- [Samples](references/samples.md)
- [Workflow Recipes](references/workflow-recipes.md)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw Slash Commands](https://docs.openclaw.ai/tools/slash-commands)
- [OpenClaw Skills Config](https://docs.openclaw.ai/tools/skills-config)
- [OpenClaw Creating Skills Guide](https://docs.openclaw.ai/tools/creating-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON manifests, Python and TypeScript starter code, and shell command plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dry-run artifacts such as storyboards, provider routing summaries, Remotion manifests, and executable API plans for user review.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
