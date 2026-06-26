## Description: <br>
Convert any webpage to a clean, high-quality PDF file and send it directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huchiyv](https://clawhub.ai/user/huchiyv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill when they need a webpage exported as a readable PDF file for viewing, saving, or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may lead an agent to export authenticated or sensitive webpages. <br>
Mitigation: Use the skill only when the user clearly requests a PDF export, and avoid authenticated or sensitive pages unless the request explicitly authorizes export. <br>
Risk: Cleanup instructions use direct shell deletion of a generated PDF path. <br>
Mitigation: Review the cleanup path before running deletion and remove only the exported PDF after it has been sent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huchiyv/web-to-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown instructions with inline tool commands and a generated PDF file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow creates a local webpage PDF, sends it to the user, and then removes the local copy.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
