## Description: <br>
Generates AI videos through the SeaArt platform from text prompts or image URLs using supported video models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seaartpublic](https://clawhub.ai/user/seaartpublic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure SeaArt authentication, submit text-to-video or image-to-video requests, and retrieve the generated video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SeaArt session token and sends prompts, image URLs, and the token to SeaArt. <br>
Mitigation: Install only if you trust the publisher and SeaArt; keep SEAART_TOKEN in a private configuration location, do not paste or print it in chat or logs, and rotate or remove it when no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/seaartpublic/seaart-video-public) <br>
- [SeaArt platform](https://www.seaart.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and returned video URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts, image URLs, and the SeaArt session token are sent to SeaArt to generate and poll video tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
