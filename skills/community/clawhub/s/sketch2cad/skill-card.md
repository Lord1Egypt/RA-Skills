## Description:

Sketch2CAD converts dimensioned hand-drawn sketches into editable AutoCAD-compatible DXF files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdszeyao](https://clawhub.ai/user/cdszeyao)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, and CAD practitioners use this skill to turn dimensioned hand-drawn outlines into editable DXF drawings for CAD cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted output filename can be injected into dynamically executed Python in the converter.

Mitigation: Restrict output paths to a controlled DXF output directory and stop building executable Python from user-controlled filenames before installing or using the skill.

Risk: The converter installs an unpinned ezdxf package at runtime.

Mitigation: Move ezdxf to a pinned, reviewed dependency installed outside normal runtime.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cdszeyao/skills/sketch2cad)
- [Skill Instructions](artifact/SKILL.md)
- [Primary Converter Script](artifact/scripts/convert.py)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Files]

**Output Format:** [DXF file plus concise Markdown status and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates AutoCAD R2010-compatible DXF linework from ordered x,y coordinates; units default to millimeters.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
