## Description:

Use when choosing a DESIGN.md style, applying a style to a web project, generating page prompts or template recipes, browsing bundled source systems, or checking UI code against a selected visual style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwei1125](https://clawhub.ai/user/liuwei1125)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design-focused coding agents use Vibe UI to select visual styles, apply DESIGN.md guidance, generate page-specific UI prompts, and review generated web UI for design consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-local workflows can write DESIGN.md, DESIGN.generated.md, .vibe-ui JSON files, reports, and preview outputs into the current project.

Mitigation: Run the skill only in projects where these local design artifacts are expected, review generated files before committing them, and choose explicit output paths for report or preview commands.

Risk: The optional extract-url workflow can fetch arbitrary HTTP or HTTPS URLs.

Mitigation: Do not run extract-url against untrusted, internal, localhost, metadata-service, or redirected URLs.

Risk: Optional package or lint commands may execute project tooling through npx or npm scripts.

Mitigation: Review package commands and dependency execution prompts before allowing package execution.

## Reference(s):

- [Vibe UI ClawHub skill page](https://clawhub.ai/liuwei1125/skills/vibe-ui)
- [README.md](README.md)
- [Third Party Notices](resource/open-design-attribution.md)
- [Resource Sync Manifest](resource/resources-sync-manifest.json)
- [SECURITY.md](SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, generated DESIGN.md files, JSON state files, and design review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes project-local DESIGN.md and .vibe-ui files for selected workflows; optional reports and browser previews are written to user-selected output paths.]

## Skill Version(s):

1.1.0 (source: package.json, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
