## Description:

Headless creative production studio for AI agents that generates images, edits photos, creates videos, produces voiceover, music, and SFX, and assembles polished output via Remotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cohnen](https://clawhub.ai/user/cohnen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to run agent-driven image, video, audio, storyboard, and Remotion assembly workflows for product videos, social ads, explainers, marketing assets, and visual/audio content pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send briefs, images, audio, and other user content to external AI providers.

Mitigation: Use only content approved for those providers, prefer an explicit --provider selection, and run --dry-run before making API calls.

Risk: Remotion init, render, and pipeline workflows can run npm or npx project code with weak scoping.

Mitigation: Run Remotion workflows only against trusted or sandboxed projects with pinned dependencies.

Risk: The security evidence verdict is suspicious because the skill combines external provider calls with executable project workflows.

Mitigation: Review the skill before installing and avoid sensitive briefs or media unless the environment and provider terms are approved.

## Reference(s):

- [ShellBot Homepage](https://getshell.ai)
- [Command Reference](references/command-reference.md)
- [Provider Matrix](references/provider-matrix.md)
- [Remotion Playbook](references/remotion-playbook.md)
- [Creative Guidelines](references/creative-guidelines.md)
- [Prompt Cookbook](references/prompt-cookbook.md)
- [Workflow Recipes](references/workflow-recipes.md)
- [Template Showcase](references/template-showcase.md)
- [Remotion Rules Index](references/remotion-rules-index.md)
- [Freepik API Keys](https://www.freepik.com/api/keys)
- [fal.ai API Keys](https://fal.ai/dashboard/keys)
- [Google AI Studio API Keys](https://aistudio.google.com/apikey)
- [OpenRouter API Keys](https://openrouter.ai/keys)
- [OpenRouter Image Models](https://openrouter.ai/collections/image-models)
- [ElevenLabs API Keys](https://elevenlabs.io/app/settings/api-keys)

## Skill Output:

**Output Type(s):** [JSON, Files, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON command output, generated media files, Markdown guidance, shell commands, and Remotion project code/configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands support dry-run previews and may track asynchronous provider tasks in .creative-tasks.jsonl.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
