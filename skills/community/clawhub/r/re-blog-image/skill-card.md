## Description: <br>
Generate a 1600px-wide WebP blog thumbnail image using the nano-img CLI when a user provides a blog topic or blog name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dishant0406](https://clawhub.ai/user/dishant0406) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and site operators use this skill to generate a blog thumbnail from a topic and record the resulting image path in local blog metadata when a matching metadata file exists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill checks NANO_IMAGE_API_KEY in ways that can expose credential values in terminal output. <br>
Mitigation: Verify that the variable is present without printing the secret value, and keep credentials out of completion reports and logs. <br>
Risk: The skill may install or invoke the nano-img/nanobana CLI and send prompts to an external image service. <br>
Mitigation: Review the CLI package and service terms before use, run it in an environment appropriate for external API calls, and avoid including sensitive information in image prompts. <br>
Risk: The skill can modify local blog metadata files after generation. <br>
Mitigation: Review the matched ~/blog-meta/*.json file before and after the run, and confirm only the intended thumbnail_path field changed. <br>


## Reference(s): <br>
- [Image Generation Reference](references/image-generation.md) <br>
- [Re Blog Image on ClawHub](https://clawhub.ai/dishant0406/re-blog-image) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Markdown, Configuration guidance] <br>
**Output Format:** [WebP image file, JSON metadata update, and Markdown/text completion report with shell command details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a 1600px-wide WebP thumbnail and may update the thumbnail_path field in a matching ~/blog-meta/*.json file.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
