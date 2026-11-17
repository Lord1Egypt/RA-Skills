## Description:

Generates videos from text prompts with optional first-frame image input, prints the generated video URL, and downloads the resulting video file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warm-wm](https://clawhub.ai/user/warm-wm)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and content builders use this skill to run a Volcengine Ark video-generation script from an agent workflow, providing an output filename, prompt, and optionally a URL or local file for the first frame.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-supplied local first-frame path can be read and sent to an external video API without validating that the file is an image.

Mitigation: Use only dedicated, non-sensitive image files for first-frame inputs; avoid passing sensitive local paths and review file paths before execution.

Risk: The skill depends on external Volcengine Ark credentials and service calls.

Mitigation: Keep credentials in environment variables, avoid placing secrets in prompts or source files, and run the script only in trusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/warm-wm/skills/volcengine-video-generate)
- [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; runtime output includes console text, a video URL, and a downloaded video file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires API credentials through environment variables such as MODEL_VIDEO_API_KEY or ARK_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
