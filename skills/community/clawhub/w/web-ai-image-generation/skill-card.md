## Description: <br>
Automates Gemini or ChatGPT web image generation through a logged-in browser profile, submits prompts, waits for generated images, and saves the resulting image files locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henryczq](https://clawhub.ai/user/henryczq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation operators use this skill to generate cover, marketing, short-video, or prompt-driven images from Gemini or ChatGPT without calling image APIs directly. It is useful when a workflow needs to reuse a dedicated browser login profile and download generated images into a local directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The browser profile can contain login cookies and account state for Gemini or ChatGPT. <br>
Mitigation: Use a dedicated profile for this skill instead of an everyday browser profile. <br>
Risk: Prompts and generated outputs may include sensitive or regulated data. <br>
Mitigation: Do not send secrets or regulated data in prompts, and keep the output directory private. <br>
Risk: Unpinned Python dependencies can change behavior over time. <br>
Mitigation: Pin dependency versions before production use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/henryczq/web-ai-image-generation) <br>
- [DEPENDENCIES.md](artifact/DEPENDENCIES.md) <br>
- [requirements.txt](artifact/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown instructions with shell command examples; runtime output is local JPEG image files and printed file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a desktop-capable browser environment, Playwright dependencies, and a dedicated Gemini or ChatGPT browser profile for saved login state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
