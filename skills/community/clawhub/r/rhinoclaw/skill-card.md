## Description: <br>
Control Rhino 3D via AI agents with tools for geometry, transforms, booleans, PBR materials, Grasshopper automation, VisualARQ BIM objects, viewport control, parametric modeling, architectural layouts, and IFC export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[McMuff86](https://clawhub.ai/user/McMuff86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and engineers use RhinoClaw to automate Rhino 3D modeling workflows from an agent, including CAD geometry creation, object transforms, rendering, Grasshopper definition execution, and optional VisualARQ BIM workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad model-editing authority can modify or damage active Rhino files. <br>
Mitigation: Use the skill only with trusted prompts and recoverable Rhino files, and keep backups before running commands that create, delete, transform, save, import, or export model content. <br>
Risk: Python execution and raw command paths can be unsafe when driven by untrusted prompts or scripts. <br>
Mitigation: Review generated Python, shell commands, and RhinoClaw command arguments before execution, especially script execution, Grasshopper automation, file operations, and destructive object edits. <br>
Risk: Remote exposure of the RhinoClaw TCP port can expand access to the running Rhino session. <br>
Mitigation: Prefer local-only access where possible and avoid exposing the TCP port beyond trusted local, WSL, LAN, or VPN environments. <br>
Risk: Screenshots and renders may reveal hidden or sensitive model content. <br>
Mitigation: Inspect the Rhino scene and capture settings before sharing generated screenshots or rendered files. <br>


## Reference(s): <br>
- [RhinoClaw Skill Page](https://clawhub.ai/McMuff86/rhinoclaw) <br>
- [McMuff86 Publisher Profile](https://clawhub.ai/user/McMuff86) <br>
- [RhinoClaw Command Reference](artifact/references/commands.md) <br>
- [VisualARQ API Learnings](artifact/references/visualarq-learnings.md) <br>
- [GH Script Templates](artifact/templates/ghscripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python command invocations, JSON configuration, and generated CAD automation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may direct RhinoClaw scripts to modify an active Rhino document, run Grasshopper definitions, export files, or capture viewport images.] <br>

## Skill Version(s): <br>
0.2.6 (source: server release evidence; artifact frontmatter lists 0.2.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
