## Description: <br>
AI-ready skill to extract long-form X (Twitter) articles and convert them into clean Markdown files using headless browser technology. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caol64](https://clawhub.ai/user/caol64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to extract long-form X (Twitter) articles from a provided URL and save the content as clean Markdown for reading, archiving, or downstream agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a third-party Python package and downloads Chromium browser components on first execution. <br>
Mitigation: Install and run it in an isolated environment, and allow network access only to the target X article and Playwright browser mirrors. <br>
Risk: Browser automation and dependency install scripts can expose local data if run in a sensitive environment. <br>
Mitigation: Avoid running the skill on systems that contain sensitive local data or credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caol64/x-article-to-markdown) <br>
- [GitHub repository referenced by artifact](https://github.com/caol64/omni-article-markdown) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown files and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves original image URLs and converts quoted posts into Markdown links when extraction succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
