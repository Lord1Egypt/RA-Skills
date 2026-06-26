## Description: <br>
Generates PNG cover, poster, social media, and illustration images from a user-provided topic by filling local HTML templates and rendering them with Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoyuhyy](https://clawhub.ai/user/luoyuhyy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to generate local PNG image assets for covers, posters, social media posts, and visual materials from short topic prompts with selectable styles and sizes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local browser renderer and writes PNG files to local storage. <br>
Mitigation: Install only when local Playwright rendering and local file output are acceptable for the workspace. <br>
Risk: Untrusted HTML or JavaScript inserted into template placeholders could change rendered output or browser behavior. <br>
Mitigation: Treat image fields as plain text, avoid pasting untrusted HTML or JavaScript into placeholders, and review template changes before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luoyuhyy/xhs-html-cover) <br>
- [Playwright documentation](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image files with Markdown usage guidance and Playwright screenshot commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports multiple visual styles and aspect ratios; generated images are written locally.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
