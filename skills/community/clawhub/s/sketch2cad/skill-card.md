## Description: <br>
Sketch2CAD converts dimensioned hand-drawn sketches into editable AutoCAD-compatible DXF files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdszeyao](https://clawhub.ai/user/cdszeyao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and field teams use this skill to turn clear dimensioned sketch photos into DXF files for CAD editing and drafting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter creates a persistent Python virtual environment and downloads ezdxf from pip on first use, which may affect supply-chain review and reproducibility. <br>
Mitigation: Install and run the skill only in an approved environment, and review or pin the dependency before deployment where required. <br>
Risk: User-controlled or unusual output filenames could cause generated DXF files to be written somewhere unintended. <br>
Mitigation: Use a controlled output directory and simple reviewed filenames for generated DXF files. <br>
Risk: Sensitive building sketches may be exposed during image analysis or when generated files are shared through Feishu. <br>
Mitigation: Avoid sensitive plans unless the image analysis and file-sharing path are approved for that data. <br>


## Reference(s): <br>
- [Sketch2CAD ClawHub page](https://clawhub.ai/cdszeyao/sketch2cad) <br>
- [Converter script](artifact/scripts/convert.py) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [DXF file with markdown or text guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates closed 2D polylines from ordered x,y coordinates in millimeters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
