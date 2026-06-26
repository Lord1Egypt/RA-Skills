## Description: <br>
Converts Figma designs into frontend component code by running the Sloth D2C CLI, processing generated chunks, and writing final project files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cherokeeli](https://clawhub.ai/user/cherokeeli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to turn a specified Figma file and node into frontend project code, with optional framework selection and follow-up chunk aggregation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires access to the target Figma file and may use sensitive Figma credentials. <br>
Mitigation: Use least-privileged Figma credentials and provide access only to the design files needed for the conversion. <br>
Risk: The workflow depends on the Sloth CLI/npm package and executes it in the target workspace. <br>
Mitigation: Install and run the skill only if you trust the Sloth CLI package, preferably on a branch or disposable workspace. <br>
Risk: Generated code and .sloth chunks may be incorrect or may include design-derived content that should not be shared. <br>
Mitigation: Review generated files and .sloth chunks before committing, deploying, or sharing the output. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON parsing steps, and generated code or project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Figma file key and node ID; may write generated project files and reviewable .sloth chunks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
