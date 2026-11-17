## Description:

Authoring and debugging scripts for Rhinoceros 3D, including RhinoScript, RhinoPython, RhinoCommon scripts, command macros, geometry and document automation, viewport selection, redraw, undo, and Script Editor workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and technical artists use this skill to draft, review, and troubleshoot Rhino automation for modeling workflows, including scripts, command macros, object manipulation, RhinoCommon usage, loading, startup, and distribution patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Rhino macros or scripts can modify or delete model content.

Mitigation: Review proposed automation before running it, save work first, and test destructive commands on disposable copies.

Risk: Startup scripts, aliases, and search paths can persist automation across Rhino sessions.

Mitigation: Install only from trusted locations and audit startup entries, aliases, and search paths after changes.

Risk: Temp-file based workflows can leave stale inputs or outputs behind.

Mitigation: Use explicit file paths, validate the expected input before execution, and clean temporary files after use.

## Reference(s):

- [rhinoscriptsyntax Cheatsheet](references/rhinoscriptsyntax-cheatsheet.md)
- [RhinoCommon Namespace Map](references/rhinocommon-map.md)
- [Macros, Loading, and Running Scripts](references/macros-and-loading.md)
- [VBScript Quirks for RhinoScript](references/vbscript-quirks.md)
- [Methods and Functions](references/methods-and-functions.md)
- [VBScript Methods](references/vbscript-methods.md)
- [RhinoScript landing](https://docs.mcneel.com/rhino/8/help/en-us/information/rhinoscripting.htm)
- [Rhino Developer Hub](https://developer.rhino3d.com/)
- [RhinoCommon API Index](https://mcneel.github.io/rhinocommon-api-docs/api/RhinoCommon/html/R_Project_RhinoCommon.htm)
- [Rhino Developer Samples: RhinoScript](https://github.com/mcneel/rhino-developer-samples/tree/8/rhinoscript)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, command macro snippets, and concise troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include RhinoPython, RhinoScript/VBScript, C# RhinoCommon snippets, Rhino command macros, loading instructions, and review notes.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
