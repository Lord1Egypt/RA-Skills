## Description: <br>
Sprite Tools helps agents prepare shell workflows and helper code for splitting sprite-sheet grids and trimming image backgrounds into individual PNG, JPG, or WebP assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical artists, and agent users can use this skill to split generated sprite sheets, crop transparent or fixed-color borders, and prepare image assets for game or art pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional remove.bg workflow can upload selected local images to an external service. <br>
Mitigation: Use that workflow only when external processing is acceptable, and avoid it for proprietary, confidential, unreleased, or regulated assets unless the publisher adds clear opt-in and data-handling disclosure. <br>


## Reference(s): <br>
- [Sprite Tools ClawHub Release](https://clawhub.ai/axelhu/sprite-tools) <br>
- [remove.bg API endpoint referenced by the skill](https://api.remove.bg/v1.0/removebg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include commands that create image files in a specified directory or /tmp/sprite_out/.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
