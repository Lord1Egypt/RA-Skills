## Description: <br>
Generate, vectorize, upscale, replace background, variate, remove background, and transform images via Recraft API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nkrcrft](https://clawhub.ai/user/nkrcrft) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and content creators use this skill to generate images and transform existing image files through the Recraft API from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images are sent to Recraft for processing. <br>
Mitigation: Avoid confidential or regulated content unless Recraft is approved for that data. <br>
Risk: Generated files can overwrite paths chosen by the user. <br>
Mitigation: Use a dedicated output folder and timestamped filenames before running generation or edit commands. <br>
Risk: The user-info command may print account email or credit details into shared logs. <br>
Mitigation: Avoid running user-info in shared sessions or logs unless that account information is acceptable to disclose. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nkrcrft/recraft-ai) <br>
- [Recraft](https://www.recraft.ai/) <br>
- [Recraft API key page](https://www.recraft.ai/profile/api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, API Calls, Guidance] <br>
**Output Format:** [Saved image or SVG files with text status output and MEDIA path lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, Python 3.10 or newer, and RECRAFT_API_TOKEN; output files are written to user-selected paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
