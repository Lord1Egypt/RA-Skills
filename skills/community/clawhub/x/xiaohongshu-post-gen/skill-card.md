## Description: <br>
Generate complete Xiaohongshu (Little Red Book) posts with up to 10 pages (3:4 vertical format). Auto-parses text content into cover + content pages. Supports 4 styles (dreamy, tech, minimal, warm). Uses Gemini 3.1 Flash Image Preview via nano-banana-2-direct. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content creators use this skill to turn a title, optional subtitle/date, and post content into multi-page Xiaohongshu image posts with consistent layouts and visual styles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provided post content is sent to Google's Gemini service for image generation. <br>
Mitigation: Avoid confidential or regulated content and use a dedicated Gemini API key for this workflow. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; generated PNG image files when the script is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and sends provided post title, subtitle, date, and content to Google's Gemini service for image generation.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
