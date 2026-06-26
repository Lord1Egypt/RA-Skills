## Description: <br>
Generate videos with a locally running SGLang-Diffusion server that has a video model loaded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangyukunok](https://clawhub.ai/user/jiangyukunok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to submit text-to-video or image-to-video prompts to a trusted local SGLang-Diffusion server, monitor asynchronous generation, and save the resulting MP4 path for the agent to return. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts or input images may be sent to a SGLang-Diffusion server outside the user's control. <br>
Mitigation: Use only a trusted server and avoid sending private prompts or images to untrusted endpoints. <br>
Risk: API keys can be exposed if passed or stored carelessly. <br>
Mitigation: Keep the SGLANG_DIFFUSION_API_KEY private and avoid sharing command history or configuration files containing secrets. <br>
Risk: The script writes the downloaded video to the selected output path. <br>
Mitigation: Choose output paths deliberately and verify the saved location before sharing or using the generated MP4. <br>


## Reference(s): <br>
- [SGLang project](https://github.com/sgl-project/sglang) <br>
- [ClawHub skill page](https://clawhub.ai/jiangyukunok/sglang-diffusion-video) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Text output with shell command examples and a saved MP4 media path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a trusted SGLang-Diffusion server; output defaults to a timestamped MP4 in /tmp unless an output path is provided.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
