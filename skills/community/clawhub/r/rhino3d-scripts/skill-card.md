## Description: <br>
Authoring and debugging scripts for Rhinoceros 3D (Rhino 8 and later), including RhinoScript, RhinoPython, RhinoCommon-based scripts, command macros, geometry and document automation, viewport selection, redraw and undo control, and loading scripts from the Rhino Script Editor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhauga](https://clawhub.ai/user/jhauga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and technical artists use this skill to write, edit, troubleshoot, and distribute Rhino automation using RhinoPython, RhinoScript/VBScript, RhinoCommon, and command macros. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Rhino scripts or macros can delete or bulk-edit model objects when run in Rhino. <br>
Mitigation: Review generated scripts and macros before execution, especially commands that delete, transform, or bulk-edit document objects. <br>
Risk: Startup scripts and aliases can run automatically or repeatedly in a Rhino environment. <br>
Mitigation: Review scripts before adding them to Rhino startup lists, aliases, toolbar buttons, or shared search paths. <br>
Risk: Long-running Rhino automation can make Rhino appear frozen or leave redraw disabled after an error. <br>
Mitigation: Use cancellation checks for long loops and wrap redraw changes in try/finally blocks so view redraw is restored. <br>


## Reference(s): <br>
- [Rhino 3D Scripts on ClawHub](https://clawhub.ai/jhauga/rhino3d-scripts) <br>
- [rhinoscriptsyntax Cheatsheet](references/rhinoscriptsyntax-cheatsheet.md) <br>
- [RhinoCommon Namespace Map](references/rhinocommon-map.md) <br>
- [Macros, Loading, and Running Scripts](references/macros-and-loading.md) <br>
- [VBScript Quirks for RhinoScript](references/vbscript-quirks.md) <br>
- [VBScript Methods](references/vbscript-methods.md) <br>
- [Methods and Functions](references/methods-and-functions.md) <br>
- [RhinoScript landing](https://docs.mcneel.com/rhino/8/help/en-us/information/rhinoscripting.htm) <br>
- [Rhino Developer Hub](https://developer.rhino3d.com/) <br>
- [RhinoCommon API index](https://mcneel.github.io/rhinocommon-api-docs/api/RhinoCommon/html/R_Project_RhinoCommon.htm) <br>
- [Rhino developer samples](https://github.com/mcneel/rhino-developer-samples/tree/8/rhinoscript) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with RhinoPython, VBScript, C#, and Rhino command macro code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include script review notes, troubleshooting guidance, Rhino startup or alias configuration steps, and command macro examples.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
