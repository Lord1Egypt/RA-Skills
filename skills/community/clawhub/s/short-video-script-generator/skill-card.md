## Description: <br>
Generates Chinese short-video scripts for multiple platforms, including hooks, shot outlines, voiceover copy, subtitle text, background music suggestions, calls to action, and script management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baolige2023](https://clawhub.ai/user/baolige2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and social media operators use this skill to generate platform-specific short-video scripts from a topic, target platform, and duration. It is intended for drafting Chinese video content with structured creative elements and exportable script text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds live-looking service keys and may expose third-party billing or AI service credentials. <br>
Mitigation: Rotate or remove embedded keys and configure credentials outside the distributed artifact before use. <br>
Risk: Billing can be triggered through broad automatic request handling rather than only an explicit generation action. <br>
Mitigation: Require clear user confirmation before charging and review the billing behavior before installation. <br>
Risk: Generated topics and prompts are processed by a third-party AI service. <br>
Mitigation: Use only after accepting third-party AI processing and avoid submitting sensitive or confidential prompts. <br>
Risk: Script history storage and retention are not clearly documented. <br>
Mitigation: Document where generated script history is stored, how long it is retained, and how users can delete it. <br>
Risk: The application is configured for public binding and debug operation. <br>
Mitigation: Disable debug mode and avoid public network binding for normal deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baolige2023/short-video-script-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Structured script content with optional Markdown or text export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include hook text, shot descriptions, voiceover copy, subtitle text, background music suggestions, and CTA guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
