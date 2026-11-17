## Description:

Export and import SOUL packages for OpenClaw agents. Use when creating a reusable persona package (SOUL.md + preview.md + manifest.json), installing a soul package into a new/existing agent workspace, or batch listing local soul packages for a Soul marketplace workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juan-xin-cai](https://clawhub.ai/user/juan-xin-cai)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to export reusable SOUL persona packages, import them into agent workspaces, and list local soul packages for marketplace-style workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported SOUL packages can add unreviewed agent instructions to a workspace.

Mitigation: Install only trusted packages, review SOUL.md before import, and validate behavior with a test agent first.

Risk: Using --force can overwrite an existing workspace SOUL.md.

Mitigation: Avoid --force unless the workspace has been backed up and the overwrite is intentional.

Risk: Exported archives can include local workspace paths in package metadata and preview text.

Mitigation: Review archives before sharing and avoid distributing packages when embedded local paths are sensitive.

## Reference(s):

- [Soul Pack on ClawHub](https://clawhub.ai/juan-xin-cai/skills/soul-pack)
- [Soul Package Manifest Schema](schema/manifest.schema.v0.1.json)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with bash commands and generated package files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports SOUL.md, preview.md, manifest.json, and tar.gz archives; imports can write SOUL.md, preview.md, and soul-manifest.json into a workspace.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
