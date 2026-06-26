## Description: <br>
Generate an Xcode SF Symbol asset catalog .symbolset from an SVG. Use when you need to add a custom SF Symbol (build-time) by creating the symbolset folder, Contents.json, and SVG file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[svkozak](https://clawhub.ai/user/svkozak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to create custom SF Symbol .symbolset assets for Xcode projects from SVG source files, including Contents.json and symbol SVG output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Bash or Node scripts that write generated files into an Xcode project tree. <br>
Mitigation: Confirm the symbol name, source SVG path, and asset catalog directory before running it, then review the generated .symbolset files before committing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/svkozak/sfsymbol-generator) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and generated Xcode asset files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local .symbolset folders containing Contents.json and SVG files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
