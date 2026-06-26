## Description: <br>
Captures a requested public web page as a viewport or full-page screenshot and can export the page as a PDF using Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiaonvmo-maker](https://clawhub.ai/user/jiaonvmo-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and content reviewers use this skill to capture public web pages for visual checks, reporting, archiving, and PDF export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens whatever URL the user provides in a headless browser, which can expose the execution environment to untrusted pages or private network targets. <br>
Mitigation: Avoid localhost, intranet, cloud metadata, authenticated, or sensitive private URLs unless that access is intentional. <br>
Risk: Login-gated or anti-automation pages may render blank, incomplete, or misleading captures. <br>
Mitigation: Review generated screenshots or PDFs before relying on them, and use an authenticated browser or site API when public rendering is insufficient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiaonvmo-maker/web-screenshot) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [PNG or JPG screenshots, PDF files, and shell status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports viewport screenshots, full-page screenshots, and A4 PDF export.] <br>

## Skill Version(s): <br>
1.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
