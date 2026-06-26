## Description: <br>
Video Pro is a commercial AI video generation skill for creating short videos from text with batch generation, templates, and voice options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cza999](https://clawhub.ai/user/cza999) <br>

### License/Terms of Use: <br>
Commercial software - requires authorization <br>


## Use Case: <br>
External creators, marketers, educators, and business users use this skill to generate short-form videos from scripts, select video templates and voices, and run single or batch generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: License keys, customer identifiers, machine identifiers, and script prompts may be stored in plaintext under ~/.video-pro and ~/openclaw-video-pro/logs. <br>
Mitigation: Use non-confidential prompts where possible, protect or delete those local files after use, and avoid shared machines for activation or generation. <br>
Risk: The skill depends on an external OpenClaw video repository and npm dependencies that are not fully represented in the package evidence. <br>
Mitigation: Inspect and pin the external repository and npm dependencies before installation or production use. <br>
Risk: The artifacts make privacy and licensing claims that the server security summary says are stronger than the available evidence supports. <br>
Mitigation: Confirm privacy handling, retention, and commercial license terms with the publisher before using generated videos commercially. <br>
Risk: The workflow requires an OpenAI API key and can generate usage costs. <br>
Mitigation: Use a dedicated API key with spending limits and monitor batch generation jobs before enabling high-volume runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cza999/video-pro-cza) <br>
- [Publisher profile](https://clawhub.ai/user/cza999) <br>
- [Template system documentation](templates/README.md) <br>
- [Artifact metadata repository link](https://github.com/cza999/video-pro) <br>
- [Declared OpenClaw video dependency](https://github.com/ZhenRobotics/openclaw-video.git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands; generated artifacts are MP4 video files and JSON reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local shell execution, an OpenAI API key, Node.js/npm dependencies, and optional commercial license activation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
