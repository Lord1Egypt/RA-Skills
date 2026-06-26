## Description: <br>
Automatically converts Markdown reports to PDF before sending them so WeChat and Feishu users can view them directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingxxxxx](https://clawhub.ai/user/jingxxxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs to deliver Markdown reports as PDFs for WeChat, Feishu, or other channels where Markdown rendering is unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The conversion command may fetch and run md-to-pdf through npm at use time. <br>
Mitigation: Use this in environments where runtime npm execution is acceptable, or preinstall and pin a vetted converter for stricter environments. <br>
Risk: PDF conversion can fail or produce imperfect layout for complex tables, code blocks, or font-dependent Chinese content. <br>
Mitigation: Check that the PDF exists and is non-empty before sending it, review important reports, and send the original Markdown with a notice if conversion fails. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with an inline bash command and generated PDF output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a PDF next to the source Markdown file and falls back to sending the original Markdown if conversion fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
