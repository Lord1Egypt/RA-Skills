## Description: <br>
Builds or reuses compact navigation indexes for large, multi-file, or layered skills so agents can load only the relevant sections instead of rereading full sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoh51918-lgtm](https://clawhub.ai/user/haoh51918-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create or reuse a workspace-local index for large skills, reducing repeated source reads while keeping original skill files authoritative. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script can write outside the intended index directory if given an unsafe skill ID. <br>
Mitigation: Review before installing if agents may run bundled scripts; use simple slug-like skill IDs, avoid path separators or `..`, and inspect generated `.skill-index` files before relying on them. <br>


## Reference(s): <br>
- [Initial Mapping](references/initial-mapping.md) <br>
- [Lookup Patterns](references/lookup-patterns.md) <br>
- [Map Layout](references/map-layout.md) <br>
- [Map Quality](references/map-quality.md) <br>
- [Mapping Policy](references/mapping-policy.md) <br>
- [Refresh Policy](references/refresh-policy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and generated workspace index files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create `.skill-index/registry.json` and `.skill-index/skills/<skill-id>/index.md` in the workspace root when the scaffold script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
