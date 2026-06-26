## Description: <br>
Detects unhealthy coupling between components, services, or layers that have become unable to change independently, and maps coupling health across the system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and architecture reviewers use this skill to identify unhealthy coupling, change-lock patterns, deploy dependencies, and decoupling priorities across software components. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Architecture reports for private repositories may include sensitive component names, internal design details, or operational relationships. <br>
Mitigation: Limit analysis to the intended repository and remove secrets, private logs, and unrelated files from any shared report. <br>
Risk: Coupling assessments may be incomplete if the agent cannot access full dependency, deployment, change-history, or failure-correlation evidence. <br>
Mitigation: Review findings with maintainers and validate recommendations against source control, deployment, and incident data before making architecture changes. <br>


## Reference(s): <br>
- [Tidal Lock skill page](https://clawhub.ai/jcools1977/tidal-lock) <br>
- [Publisher profile](https://clawhub.ai/user/jcools1977) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown analysis report with coupling severity, lock clusters, change-correlation findings, and decoupling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only architecture review output; no API calls or executable code are included in the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
