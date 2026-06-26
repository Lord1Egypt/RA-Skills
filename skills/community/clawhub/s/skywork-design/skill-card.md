## Description: <br>
Skywork Design generates or edits images via the Skywork Image API for image creation, poster design, logo design, visual asset generation, and image modification with aspect ratio and resolution control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxcun17](https://clawhub.ai/user/gxcun17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, marketers, and developers use this skill to generate or edit visual assets such as posters, logos, product images, social media graphics, storyboards, brochures, and branded materials through the Skywork Image API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images are sent to Skywork's cloud service. <br>
Mitigation: Use the skill only with data approved for Skywork processing, and avoid sensitive images unless that service is approved for the data. <br>
Risk: The SKYWORK_API_KEY can enable API use if exposed. <br>
Mitigation: Use a dedicated key where possible, avoid printing or screenshotting it, and rotate the key if exposure is suspected. <br>
Risk: Membership upgrade links may involve payment or account changes. <br>
Mitigation: Manually verify any upgrade link before paying or changing account status. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gxcun17/skywork-design) <br>
- [Publisher Profile](https://clawhub.ai/user/gxcun17) <br>
- [Skywork AI](https://skywork.ai) <br>
- [API Key Setup](references/apikey-fetch.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, generated image file paths, and image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and SKYWORK_API_KEY; supports prompt, filename, optional input images, aspect ratio, and 1K, 2K, or 4K resolution.] <br>

## Skill Version(s): <br>
1.0.8 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
