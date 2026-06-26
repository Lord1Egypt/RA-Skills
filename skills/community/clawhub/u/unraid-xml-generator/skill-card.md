## Description: <br>
Generates Unraid DockerMan user template XML files from structured container inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashanzzz](https://clawhub.ai/user/ashanzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and homelab operators use this skill to produce Unraid DockerMan XML templates for container deployments, including configurable ports, paths, environment variables, proxy settings, and startup command handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated DockerMan XML can change container startup behavior, including image selection, volume mounts, environment variables, proxy defaults, and ENTRYPOINT/PostArgs commands. <br>
Mitigation: Inspect the generated XML before deploying it and verify the image, paths, variables, proxy settings, and startup command match the intended container behavior. <br>
Risk: Deploying a generated template to the Unraid templates directory can persist container configuration on the host. <br>
Mitigation: Use deployment only for intended Unraid template generation and confirm the target path before writing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ashanzzz/unraid-xml-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with XML snippets, shell commands, and optional generated XML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated XML may be written to stdout, a user-selected output path, or the Unraid DockerMan templates directory after confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
