## Description: <br>
An AI image-generation skill for creating high-resolution images from text prompts or reference images using the seedream 5.0 lite model through redfox.hk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, designers, content creators, and e-commerce operators use this skill to generate high-resolution images, product scenes, visual concepts, and related image sets from natural-language prompts or reference images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded reference images, and generated image URLs are sent to redfox.hk for image generation. <br>
Mitigation: Use the skill only with data appropriate for redfox.hk and avoid submitting sensitive prompts or reference images. <br>
Risk: The REDFOX_API_KEY could be exposed if placed in prompts, shared files, logs, or other plaintext outputs. <br>
Mitigation: Use a revocable REDFOX_API_KEY through an environment variable or local configuration, and keep secrets out of prompts and shared artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/seedream-5-lite) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox website](https://redfox.hk?source=github) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, task status text, and generated PNG or JPEG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY. Prompts, uploaded reference images, and generated image URLs are processed by redfox.hk. Generated images download to ~/Downloads/QoderImages by default.] <br>

## Skill Version(s): <br>
1.1.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
