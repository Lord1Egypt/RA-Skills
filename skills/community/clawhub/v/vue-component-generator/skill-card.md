## Description: <br>
Generates a basic Vue 3 single-file component template from a component name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Frontend developers can use this skill to create a starter Vue single-file component in a local project. It is most useful for quick scaffolding before manually reviewing and extending the generated component. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator writes a .vue file in the current directory and can overwrite an existing file with the same name. <br>
Mitigation: Run it from the intended project directory, use a simple component name, and check for an existing target file before execution. <br>
Risk: The documentation advertises TypeScript, SCSS, API mode, and output-directory options that the provided script does not implement. <br>
Mitigation: Treat the generated file as a basic Vue template and verify any additional options or framework conventions manually before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/vue-component-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands] <br>
**Output Format:** [Vue single-file component (.vue) plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a component file named from the first command-line argument in the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
