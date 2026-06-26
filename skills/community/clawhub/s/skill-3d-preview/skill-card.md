## Description: <br>
Creates simple 3D scene previews with ASCII rendering and Three.js HTML export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zimuge-doudou](https://clawhub.ai/user/zimuge-doudou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users can use this skill to create lightweight 3D scene descriptions, render an ASCII top-down preview, and export a local Three.js HTML preview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local scene JSON and preview HTML files. <br>
Mitigation: Run it in a restricted workspace and inspect generated files before opening, sharing, or relying on them. <br>
Risk: Generated preview HTML may include unsafe or under-validated scene values. <br>
Mitigation: Use only trusted scene names and scene JSON, and add filename validation plus HTML and JavaScript escaping before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zimuge-doudou/skill-3d-preview) <br>
- [Three.js CDN dependency](https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Code] <br>
**Output Format:** [Plain text status messages, JSON scene files, ASCII previews, and Three.js HTML preview files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update files under the skill's local scenes directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
