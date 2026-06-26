## Description: <br>
Create SVG images and convert them to PNG without external graphics libraries by writing SVG text directly and using local rsvg-convert. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LiJY2015](https://clawhub.ai/user/LiJY2015) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and agents use this skill to create custom SVG illustrations, avatars, logos, and PNG exports from SVG source files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated SVG and PNG files and runs local rsvg-convert for image conversion. <br>
Mitigation: Review target file paths and conversion commands before execution, and keep generated files inside the intended workspace. <br>
Risk: SVG inputs from untrusted sources may contain unexpected content or trigger converter behavior the user did not intend. <br>
Mitigation: Review SVG content before conversion and prefer trusted or newly generated SVG inputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LiJY2015/svg-draw) <br>
- [SVG namespace](http://www.w3.org/2000/svg) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Guidance] <br>
**Output Format:** [SVG/XML files, PNG files, and Markdown guidance with bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PNG conversion requires local rsvg-convert; width and height default to 400x400 unless provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
