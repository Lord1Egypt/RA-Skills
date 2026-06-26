## Description: <br>
Scrape employee data from a logged-in SAP SuccessFactors browser session using browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VenkataLokesh-dot](https://clawhub.ai/user/VenkataLokesh-dot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees or authorized HR operators use this skill to look up SuccessFactors employee profile details from an already logged-in browser session when they provide an employee ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive SuccessFactors HR profile data through an agent-operated logged-in browser session. <br>
Mitigation: Install and run it only with organizational authorization, use a least-privilege account or session, and request only the exact fields needed. <br>
Risk: Broad profile scraping may include compensation, personal contact, documents, performance, goals, or leave information beyond the user's immediate need. <br>
Mitigation: Avoid those categories unless separately approved, and stop when the requested visible fields have been collected. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with browser automation instructions and structured employee profile results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns only fields visible in the authorized SuccessFactors UI session.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
