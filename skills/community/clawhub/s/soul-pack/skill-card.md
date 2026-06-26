## Description: <br>
Export, import, and list SOUL packages for OpenClaw agents to manage reusable persona bundles and agent workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juan-xin-cai](https://clawhub.ai/user/juan-xin-cai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to package a workspace SOUL.md into a reusable bundle, import a bundle into an agent workspace, and list local packages for sharing or marketplace workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported SOUL packages can replace an existing persona or introduce unreviewed persona content. <br>
Mitigation: Review SOUL.md before importing, use a test workspace for packages from others, and use --force only when replacement is intended. <br>
Risk: Exported packages may include private paths or sensitive persona content. <br>
Mitigation: Inspect SOUL.md, preview.md, and manifest.json before sharing packages and remove secrets or private workspace details. <br>
Risk: Importing a package changes local workspace files and may register an OpenClaw agent. <br>
Mitigation: Run in a controlled workspace and confirm the target agent name and workspace path before execution. <br>


## Reference(s): <br>
- [Soul package manifest schema](schema/manifest.schema.v0.1.json) <br>
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>
- [ClawHub skill page](https://clawhub.ai/juan-xin-cai/soul-pack) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated package files, including SOUL.md, preview.md, manifest.json, and .tar.gz archives.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local workspace files and may register an OpenClaw agent when importing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
