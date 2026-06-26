## Description: <br>
Write valid YAML that parses predictably across languages and versions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and content authors use this skill to draft YAML that avoids common parsing surprises around type coercion, indentation, strings, comments, document structure, and YAML version differences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YAML parser and version differences can make otherwise plausible YAML parse differently across projects. <br>
Mitigation: Validate generated YAML with the exact parser and YAML version used by the target project. <br>
Risk: Unquoted ambiguous scalars such as boolean-like words, null markers, version numbers, and country codes can change data semantics. <br>
Mitigation: Quote ambiguous scalar values when the intended value is a string. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces informational YAML writing guidance; users should validate resulting YAML with the parser and YAML version used by their project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
