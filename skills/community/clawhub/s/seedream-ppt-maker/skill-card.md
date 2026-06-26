## Description: <br>
Seedream Ppt Maker generates image-based PPT decks from Markdown content using Baoyu layout and style templates with Seedream 5.0 image generation and an optional interactive confirmation workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cindypapa](https://clawhub.ai/user/cindypapa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation creators use this skill to turn structured Markdown content into image-heavy PPTX decks. It helps choose layouts and styles, preview prompts, generate images through Seedream, and assemble the final presentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install check prints part of the Seedream API key, which can expose sensitive credentials in shared terminals, logs, CI output, or support transcripts. <br>
Mitigation: Remove API-key printing before running the check in shared environments, or run it only in a private local terminal where output will not be captured. <br>
Risk: Presentation content and generated prompts are sent to Volcengine Seedream for remote image generation. <br>
Mitigation: Use the skill only with content approved for that service boundary, and prefer the interactive confirmation flow for sensitive or business material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cindypapa/seedream-ppt-maker) <br>
- [Project homepage](https://github.com/Cindypapa/baoyu-seedream-ppt) <br>
- [Baoyu layout system](https://github.com/JimLiu/baoyu-skills) <br>
- [Volcengine](https://www.volcengine.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python shell commands; generated artifacts include JSON configuration, prompt Markdown, PNG images, and PPTX files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, baoyu-infographic, python-pptx, requests, and a Volcengine Seedream API key.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
