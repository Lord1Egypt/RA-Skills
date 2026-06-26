## Description: <br>
Generates a six-slide TikTok carousel with portrait images and text overlays, creates an optional Postiz draft, and outputs a caption for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otman-ai](https://clawhub.ai/user/otman-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, marketers, and developers use this skill to generate TikTok carousel assets from a topic or persona and prepare a draft for manual review before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unpinned dependencies or incorrect API configuration could change behavior or send requests to an unintended Postiz endpoint. <br>
Mitigation: Install in a virtual environment, pin or lock dependencies before production use, and confirm POSTIZ_API_URL points to the intended Postiz API. <br>
Risk: API keys and uploaded media can expose credentials or unintended local files. <br>
Mitigation: Keep keys in environment variables or a secrets manager, and upload only generated or intentionally selected image files. <br>
Risk: Generated images and captions may be inaccurate, unsuitable, or not aligned with publishing requirements. <br>
Mitigation: Review the generated draft, images, and caption before publishing. <br>


## Reference(s): <br>
- [Skill README](artifact/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/otman-ai/tikto-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, API Calls, Shell commands, Configuration] <br>
**Output Format:** [PNG image files, caption text, optional JSON draft response, and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local slide images and a caption; optionally uploads intentionally selected images to Postiz as a private TikTok draft.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
