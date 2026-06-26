## Description: <br>
Automated roadshow/investor presentation capture to PDF. Playwright-powered, supports NetRoadShow and DealRoadShow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikker1974](https://clawhub.ai/user/nikker1974) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Playwright-based capture workflows for authorized NetRoadShow or DealRoadShow investor presentations and compile captured slide screenshots into PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates gated investor-roadshow access, legal-disclaimer acceptance, email submission, and full PDF capture. <br>
Mitigation: Run it only when authorized to access, accept terms for, and retain copies of the specific roadshow materials; manually verify the URL hostname before execution. <br>
Risk: Captured screenshots and PDFs may contain confidential investor materials. <br>
Mitigation: Use a private output directory and delete captured screenshots and PDFs when they are no longer needed. <br>
Risk: The workflow can persist the roadshow email in scripts/.env. <br>
Mitigation: Prefer a session-only NRS_EMAIL value or pass the email at runtime instead of saving it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nikker1974/roadshow-capture-skill) <br>
- [NetRoadShow practice notes](references/netroadshow-practice.md) <br>
- [OpenClaw setup guide](references/openclaw-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python scripts and shell commands; runtime scripts produce PNG screenshots and PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, Playwright, Pillow, Chromium, and an authorized NRS_EMAIL value.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
