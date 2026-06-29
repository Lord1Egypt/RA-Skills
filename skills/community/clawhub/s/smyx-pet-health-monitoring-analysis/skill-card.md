## Description: <br>
Analyzes pet camera or feeder images and videos for feeding, drinking, excretion, mental state, vomiting, and limping indicators, then returns a pet health monitoring report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and pet-care application agents use this skill to submit pet monitoring media, retrieve structured health analysis, and list cloud-stored historical reports. The report is for health reference and should not replace veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends pet camera or feeder media and report-history requests to LifeEmergence cloud services. <br>
Mitigation: Use only media that users are comfortable uploading to that service, avoid sensitive household footage, and confirm retention and deletion controls before production use. <br>
Risk: The skill silently creates or reuses an account identity and can persist tokens locally. <br>
Mitigation: Treat the local workspace database as containing authentication material and restrict access to environments approved for account-linked data. <br>
Risk: Health analysis output may be incomplete or misleading if treated as a diagnosis. <br>
Mitigation: Present results as health reference information and direct users to a veterinarian when symptoms or abnormal findings are present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pet-health-monitoring-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Pet health analysis API documentation](references/api_doc.md) <br>
- [Detailed API error reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown reports, Markdown tables, or JSON depending on detail and history-query mode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include behavior counts, abnormality flags, care suggestions, warnings, and report links.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence; artifact frontmatter reports 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
