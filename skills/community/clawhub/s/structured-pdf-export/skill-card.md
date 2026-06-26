## Description: <br>
Structured PDF Export helps agents turn structured tables, comparisons, checklists, and visual data into polished local PDF files using an HTML-to-browser-to-PDF workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huchiyv](https://clawhub.ai/user/huchiyv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill when a response would otherwise contain a large table, comparison, checklist, or visualization and should instead be delivered as a formatted PDF. It is intended for single-user or trusted environments that can run a local browser workflow and temporary HTTP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The temporary HTTP server can expose generated document content beyond the local machine if it binds to a non-local interface. <br>
Mitigation: Bind the server to localhost, for example `python3 -m http.server --bind 127.0.0.1 8888`, and only open local URLs. <br>
Risk: Generated HTML or PDFs may contain sensitive data because the skill does not provide automatic sensitive-data scanning. <br>
Mitigation: Manually review the HTML in the browser and the final PDF before sending, and avoid including secrets, credentials, or regulated personal data. <br>
Risk: Port and process management can conflict with unrelated processes in multi-user environments. <br>
Mitigation: Use the skill only in single-user or trusted environments, manually verify any process using the configured port, or switch to a user-specific port. <br>
Risk: Temporary files and the local server may remain after the workflow completes. <br>
Mitigation: Confirm the server process is stopped and remove the `.pdf-export-tmp` directory after export. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huchiyv/structured-pdf-export) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated local HTML/PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local files through an OpenClaw browser and message workflow; users must review generated content before sending.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
