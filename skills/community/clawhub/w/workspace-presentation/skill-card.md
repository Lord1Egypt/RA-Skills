## Description:

Create a React/Vite Workspace Presentation from one paper-reading source workspace or source chain for packaging, presenting, reviewing, handing off, rereading, or browsing generated paper-reading artifacts in an interactive frontend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snake-fan](https://clawhub.ai/user/snake-fan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to turn one paper-reading workspace or coherent source chain into a read-only local React/Vite presentation with source-linked summaries, structured modules, and source-file previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated local presentation can preview files from the selected paper-reading workspace, which may expose sensitive content if that workspace contains secrets or private notes.

Mitigation: Review the selected source workspace before generation and use the Presentation Source Gate to confirm exactly one intended source path and output path.

Risk: The artifact references templates and schema files that are not included, so a release installed from this artifact may be incomplete.

Mitigation: Verify the package includes the referenced templates and schema files before relying on it to scaffold or refresh a presentation.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/snake-fan/Paper-Reading-Skills/tree/main/skills/workspace-presentation)
- [ClawHub skill page](https://clawhub.ai/snake-fan/skills/workspace-presentation)
- [Publisher profile](https://clawhub.ai/user/snake-fan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with file-generation instructions, JSON presentation metadata, React/Vite app files, and shell commands for local execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates or refreshes a local presentation under {workspace-root}/presentations/{presentation-slug}/ and stops with install/run commands unless the user explicitly asks to run them.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
