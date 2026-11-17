## Description:

Turn rough video ideas into structured English or Chinese prompt packs, reference-aware sequences, continuity rules, and focused debugging loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpt-img-2](https://clawhub.ai/user/gpt-img-2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and media teams use this skill to turn brief video ideas into prompt packs, shot plans, continuity constraints, avoid lists, and targeted revision guidance for text-to-video, image-to-video, reference-to-video, and video-to-video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional MCP setup asks users to run an unpinned GitHub package through npx.

Mitigation: Install the MCP only after reviewing the source, preferably pin a reviewed commit or version, and run it with limited access to local files, credentials, and environment variables.

## Reference(s):

- [SeeVido AI video generator](https://seevido.org/ai-video-generator)
- [SeeVido models](https://seevido.org/models)
- [SeeVido prompt library](https://seevido.org/seedance-2-0-prompts)
- [SeeVido video-to-prompt tool](https://seevido.org/video-to-seedance-prompt)
- [Raw skill](https://seevido.org/skills/seevido-video-prompt-architect/SKILL.md)
- [Optional MCP source](https://github.com/gpt-img-2/seevido-prompt-mcp)
- [ClawHub listing](https://clawhub.ai/gpt-img-2/skills/seevido-video-prompt-architect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown sections for prompts, reference roles, continuity constraints, avoid lists, sequence plans, revision moves, and optional setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only by default; optional MCP helpers can structure prompts, plans, diagnostics, and SeeVido resource links when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and openclaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
