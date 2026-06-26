## Description: <br>
Set up and analyze shadow traffic testing to compare new service versions against production without user impact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to configure shadow traffic mirroring and compare production and shadow service behavior before promoting a new version. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mirroring production traffic and collecting access logs may expose sensitive data or exceed the operator's authorization. <br>
Mitigation: Confirm approval before mirroring production traffic, prefer redacted or sampled logs, store captured data in restricted locations, and delete logs after analysis. <br>
Risk: Generated Kubernetes and ingress changes may affect live cluster behavior if applied without review. <br>
Mitigation: Review all Kubernetes manifests and mirror settings before applying them to a live cluster. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash, YAML, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, analysis, and report guidance for Kubernetes-based shadow traffic testing.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
