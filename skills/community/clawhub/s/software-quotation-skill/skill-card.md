## Description: <br>
Software Quotation Skill helps agents clarify software project requirements, estimate effort, and produce structured quotation documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horisony](https://clawhub.ai/user/horisony) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External software consultants, agencies, and developers use this skill to turn client software requirements into scoped work breakdowns, person-day estimates, milestone plans, payment terms, and polished quotation documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated estimates, scope statements, and payment terms may be inaccurate or unsuitable for a specific client engagement. <br>
Mitigation: Review all quotation figures, assumptions, contract terms, and risk notes before sending the document to a client. <br>
Risk: Generated HTML can load PDF export libraries from cdnjs. <br>
Mitigation: Use the CDN-hosted libraries only when acceptable for the client data involved, or replace them with trusted local copies before sharing sensitive quotation documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/horisony/software-quotation-skill) <br>
- [html2canvas cdnjs asset](https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) <br>
- [jsPDF cdnjs asset](https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Chinese-language text, Markdown tables, and single-file HTML with embedded CSS and JavaScript] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML may include PDF export behavior through html2canvas and jsPDF.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
