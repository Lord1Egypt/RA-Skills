## Description: <br>
Generate AI videos, images, and audio with Runway API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slightly-unrelated](https://clawhub.ai/user/slightly-unrelated) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative technologists use this skill to generate Runway API examples for video, image, and audio workflows. It helps set up API-key usage, choose generation models, and handle asynchronous Runway tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the examples requires a Runway API key and may spend Runway credits. <br>
Mitigation: Store RUNWAYML_API_SECRET in a secret manager or environment variable, and review model, duration, and credit impact before making API calls. <br>
Risk: Prompts, images, audio, or video inputs may be sent to Runway or partner models. <br>
Mitigation: Avoid submitting secrets, regulated data, or sensitive personal media unless your data-handling requirements allow it. <br>


## Reference(s): <br>
- [Runway API Documentation](https://docs.dev.runwayml.com/) <br>
- [Runway Model Guide](https://docs.dev.runwayml.com/guides/models/) <br>
- [Runway Developer Portal](https://dev.runwayml.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires internet access, a Runway API key, and asynchronous task polling for generated media URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
