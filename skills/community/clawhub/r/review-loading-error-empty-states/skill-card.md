## Description: <br>
Check loading, error, empty, partial, and retry states for a UI surface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ritual](https://clawhub.ai/user/ritual) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to review UI surfaces for loading, error, empty, partial-data, slow-network, and retry behavior, then confirm handled states or report explicit gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Ritual Cloud setup may install npm tooling or connect the workspace to an external cloud service. <br>
Mitigation: Use the local checklist workflow by default and require explicit user approval before running npm install commands or initializing Ritual Cloud. <br>
Risk: Optional knowledge capture can create repository note files. <br>
Mitigation: Offer OKF note creation only when reusable knowledge is found and write files only after the user approves the exact action. <br>


## Reference(s): <br>
- [Ritual homepage](https://ritual.work) <br>
- [Open Knowledge Format overview](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional code edits, shell commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce optional OKF notes only with user approval; optional Ritual Cloud setup requires explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
