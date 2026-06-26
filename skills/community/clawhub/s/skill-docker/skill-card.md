## Description: <br>
Docker enables agents to inspect Docker image manifests and run Docker buildx workflows to initialize builders, build and push multi-platform images, and destroy builders with optional cache pruning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lentiancn](https://clawhub.ai/user/lentiancn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to inspect published Docker image tags and automate multi-platform Docker buildx setup, publishing, and cleanup from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform privileged Docker host setup and modify buildx/binfmt state. <br>
Mitigation: Review before installing on workstations or CI runners with valuable Docker state, and run only with trusted Docker contexts and builder names. <br>
Risk: The build-and-push workflow can publish images to remote registries under the provided tags. <br>
Mitigation: Confirm registry login, target image tags, target platforms, and build context before execution. <br>
Risk: Builder destruction and optional pruning can remove buildx builders and cached build resources. <br>
Mitigation: Use explicit disposable builder names and enable pruning only when cache removal is intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text] <br>
**Output Format:** [Markdown guidance with bash invocations; script results are JSON or status/error strings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Docker environment and trusted registry/build context inputs.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
