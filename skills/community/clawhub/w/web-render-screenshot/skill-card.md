## Description: <br>
Generates ultra-high-resolution PNG/JPEG screenshots from HTML content or webpages using Playwright headless Chromium. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujiaming88](https://clawhub.ai/user/wujiaming88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agents use this skill to render HTML mockups, dashboards, data visualizations, infographics, and webpage previews into legible high-resolution images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering untrusted or sensitive webpages can execute page JavaScript and make network requests in the execution environment. <br>
Mitigation: Render trusted content when possible, isolate the browser environment for untrusted pages, and avoid sensitive logged-in pages unless that execution and network behavior is acceptable. <br>
Risk: The screenshot workflow depends on Playwright and Chromium being available in the runtime. <br>
Mitigation: Install Playwright and Chromium before use or run the skill in an environment where those dependencies are already provided. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wujiaming88/web-render-screenshot) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wujiaming88) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG/JPEG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default behavior uses a 1920x1080 viewport, 4x device scale factor, full-page capture, and PNG output unless configured otherwise.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
