## Description: <br>
Urlopnik helps employees in Poland calculate leave days, prepare vacation request content, generate leave-request PDFs, and identify useful leave dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomasz-pedzierski-infinity](https://clawhub.ai/user/tomasz-pedzierski-infinity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees in Poland can use this skill to estimate remaining leave, count working days for planned time off, and produce a leave request in text or PDF form. It is also useful for planning dates around Polish public holidays and long weekends. <br>

### Deployment Geography for Use: <br>
Poland <br>

## Known Risks and Mitigations: <br>
Risk: PDF generation can change the local Python environment by installing a dependency when it is missing. <br>
Mitigation: Review before installing and use the skill only where automatic pip installs are acceptable, or preinstall reportlab in a controlled environment. <br>
Risk: Handling of employee leave details and email-sending behavior is unclear. <br>
Mitigation: Do not use real employee leave details unless the recipient, contents, retention behavior, and deletion path have been verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomasz-pedzierski-infinity/urlopnik) <br>
- [Publisher profile](https://clawhub.ai/user/tomasz-pedzierski-infinity) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown-style leave request text and PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses leave dates, leave type, and employee details as inputs.] <br>

## Skill Version(s): <br>
2.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
