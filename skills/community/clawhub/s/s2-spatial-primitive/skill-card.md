## Description: <br>
Defines a universal six-element spatial data model using natural language parameters for AI-driven smart space perception and control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-space system designers use this skill to generate a baseline JSON model for representing lighting, air, sound, electromagnetic sensing, energy, and display state in AI-driven spaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill creates or replaces s2_primitive_data/primitive_6_elements_template.json in the current working directory. <br>
Mitigation: Run it from a directory where that output path is expected, or review the directory before execution. <br>
Risk: Real-world smart-space sensor or control values added later could influence agent decisions. <br>
Mitigation: Review any populated sensor or control values before providing the generated template to agents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-spatial-primitive) <br>
- [Publisher profile](https://clawhub.ai/user/SpaceSQ) <br>
- [Space2.world](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Configuration, Guidance] <br>
**Output Format:** [JSON file with console text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates s2_primitive_data/primitive_6_elements_template.json in the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
