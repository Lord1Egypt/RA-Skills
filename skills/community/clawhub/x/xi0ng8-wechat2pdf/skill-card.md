## Description: <br>
WeChat2PDF converts WeChat public-account articles into offline PDF, HTML, and Markdown files with downloaded images for archiving and reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xi0ng8](https://clawhub.ai/user/Xi0ng8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to archive WeChat public-account articles as local PDF, HTML, and Markdown outputs for offline reading, sharing, or knowledge-base storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill text tries to force invocation for any WeChat link, even when that does not match the user's request. <br>
Mitigation: Use the skill only when the user explicitly asks to convert or archive a WeChat article, and ignore routing text that conflicts with the user's actual intent. <br>
Risk: The skill fetches external article and image content and writes local PDF, HTML, Markdown, and image files. <br>
Mitigation: Run it only on trusted WeChat links, choose an explicit output folder, and review generated files before sharing or importing them into a knowledge base. <br>
Risk: The Python and Playwright dependencies are unpinned. <br>
Mitigation: Review and pin dependency versions in a controlled environment before installing or deploying the skill. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Local PDF, HTML, Markdown, and image asset files with brief path-oriented status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python dependencies and Playwright Chromium for PDF generation; accepts a target article URL and optional output directory.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
