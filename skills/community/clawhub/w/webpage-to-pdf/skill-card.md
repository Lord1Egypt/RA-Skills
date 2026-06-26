## Description: <br>
Converts web pages and web-based slide decks into multi-page PDFs using Playwright screenshots and Pillow PDF assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pearyj](https://clawhub.ai/user/pearyj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other external users can use this skill to capture websites, articles, and web-based presentations as PDF documents for sharing, archiving, or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted output filename could cause unintended shell command execution during PDF assembly. <br>
Mitigation: Use simple output filenames without shell metacharacters and prefer a patched version that invokes Python with an argument array instead of a shell string. <br>
Risk: The skill loads and renders user-provided web pages in a headless browser. <br>
Mitigation: Use the skill only with trusted or explicitly approved URLs and review the generated PDF before relying on it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PDF file plus Markdown status and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a URL, output PDF path, viewport width and height, wait time, and maximum slide count.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
