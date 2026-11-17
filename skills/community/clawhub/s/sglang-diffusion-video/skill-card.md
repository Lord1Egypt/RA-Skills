## Description:

Generate videos through a locally running SGLang-Diffusion server with a video model loaded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangyukunok](https://clawhub.ai/user/jiangyukunok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate text-to-video or image-to-video outputs from a locally running SGLang-Diffusion server. It helps an agent provide the right Python command, optional server and API-key configuration, polling settings, and saved video path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, input images, and API keys can be sent to a user-specified SGLang-Diffusion server, including over plain HTTP.

Mitigation: Use only a trusted SGLang-Diffusion server, prefer localhost or HTTPS for remote servers, avoid command-line API keys, and do not submit private images or sensitive prompts to untrusted or plain-HTTP endpoints.

## Reference(s):

- [SGLang Project](https://github.com/sgl-project/sglang)
- [ClawHub Skill Page](https://clawhub.ai/jiangyukunok/skills/sglang-diffusion-video)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; the helper script saves an MP4 file and prints a MEDIA line with the saved path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video output defaults to a timestamped MP4 in /tmp unless the user provides an explicit output path.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
