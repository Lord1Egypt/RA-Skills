## Description: <br>
Run local ComfyUI workflows via the HTTP API. Use when the user asks to run ComfyUI, execute a workflow by file path/name, or supply raw API-format JSON; supports the default workflow bundled in assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-generation users use this skill to edit and run local ComfyUI workflow JSON, queue jobs through the local HTTP API, download model weights, and return generated images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader can install and run an unverified helper program. <br>
Mitigation: Review before installing; prefer --no-pget or install pget yourself through a trusted channel. <br>
Risk: Downloaded files may be written outside the intended model folder. <br>
Mitigation: Use only trusted model URLs, avoid --overwrite with untrusted URLs, and review resolved download paths before use. <br>
Risk: Temporary workflow files may contain private prompts. <br>
Mitigation: Clear temporary workflow files after use and avoid storing sensitive prompts in reusable workflow assets. <br>
Risk: Exposing the ComfyUI HTTP API beyond localhost can increase local service exposure. <br>
Mitigation: Keep ComfyUI bound to 127.0.0.1 unless a reviewed deployment requires otherwise. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tobeyrebecca/toby-image) <br>
- [ComfyUI repository](https://github.com/comfyanonymous/ComfyUI.git) <br>
- [pget downloader](https://github.com/replicate/pget) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Images] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script output; generated image files are returned after successful runs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may write edited workflow JSON, downloaded model files, and generated image files under the local ComfyUI installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
