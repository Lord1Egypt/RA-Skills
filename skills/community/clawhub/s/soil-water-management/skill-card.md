## Description: <br>
Provides soil science, composting, irrigation, and rainwater-harvesting guidance for improving garden soil and scaling food production beyond containers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howtousehumans](https://clawhub.ai/user/howtousehumans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Gardeners, homesteaders, and food-growing agents use this skill to test soil, choose composting methods, plan irrigation, harvest rainwater, and adapt guidance to local rules and climate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill declares filesystem access even though the reviewed artifact is guidance-only. <br>
Mitigation: Grant only the local file access required by the OpenClaw setup, and avoid broader filesystem permissions when using this skill. <br>


## Reference(s): <br>
- [USDA Cooperative Extension System](https://www.nifa.usda.gov/about-nifa/how-we-work/extension/cooperative-extension-system) <br>
- [Irrigation Association](https://www.irrigation.org/) <br>
- [American Rainwater Catchment Systems Association](https://www.arcsa.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with structured checklists and YAML-like agent state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; guidance includes jurisdiction checks for rainwater collection and unit localization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
