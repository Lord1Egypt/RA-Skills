## Description: <br>
Generate professional technical documentation from codebases, including API docs, READMEs, architecture diagrams, changelogs, and onboarding guides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanwyngaard](https://clawhub.ai/user/seanwyngaard) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to scan a project and generate client-deliverable technical documentation, including README files, API documentation, architecture overviews, changelogs, onboarding guides, OpenAPI YAML, and Mermaid diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation can expose secrets, internal URLs, credentials, database details, or architecture information from the inspected project. <br>
Mitigation: Review generated documents before publishing or sending them to clients, and remove sensitive implementation details. <br>
Risk: The skill writes generated documentation files into the workspace. <br>
Mitigation: Run it on an explicit project path and keep the repository under version control so changes can be reviewed before acceptance. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation files, OpenAPI YAML, Mermaid diagrams, and summary guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated documentation under output/docs/ or docs/ depending on the requested documentation package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
