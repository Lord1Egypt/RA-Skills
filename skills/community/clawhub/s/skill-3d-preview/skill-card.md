## Description:

Creates simple 3D scene previews with ASCII top-down rendering and Three.js HTML export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zimuge-doudou](https://clawhub.ai/user/zimuge-doudou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to draft simple 3D scene layouts, add primitive objects, preview them as ASCII maps, and export browser-viewable Three.js HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unsafe file-writing behavior in a rough preview utility.

Mitigation: Use trusted scene names only and prefer a fixed version that validates scene names and size limits before writing scene or preview files.

Risk: Exported HTML loads Three.js from cdnjs, which may be unsuitable in sensitive or offline contexts.

Mitigation: Open exported HTML only where remote CDN loading is acceptable, or use a fixed version that vendors or pins the dependency for the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zimuge-doudou/skills/skill-3d-preview)
- [Three.js r128 CDN dependency](https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js)

## Skill Output:

**Output Type(s):** [text, code, configuration, shell commands]

**Output Format:** [Plain text responses with optional JSON scene files and HTML exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes scene JSON and preview HTML under the skill's local scenes directory; exported HTML loads Three.js from cdnjs.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
