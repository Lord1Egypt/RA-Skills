## Description: <br>
Generates forensic chain of custody HTML reports for evidence management and legal compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Forensic examiners, incident response teams, corporate security practitioners, law enforcement, and legal professionals use this skill to generate structured chain of custody reports from case, evidence, handler, timestamp, and integrity-hash data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive investigation, identity, evidence-location, and integrity-hash data is sent to a third-party API provider. <br>
Mitigation: Use sanitized data for testing, confirm organizational approval before live submissions, and verify the provider's retention, access-control, logging, and deletion practices. <br>
Risk: Generated reports may be used in legal or compliance workflows where incomplete or inaccurate inputs can affect evidentiary value. <br>
Mitigation: Review generated HTML reports against source case records and evidence logs before relying on them in investigations, litigation, or audits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-chain-of-custody) <br>
- [API Documentation](https://api.mkkpro.com:8115/docs) <br>
- [Kong Route](https://api.mkkpro.com/compliance/chain-of-custody) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, html, api_calls] <br>
**Output Format:** [JSON response containing a generated HTML custody report string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires structured case metadata, evidence items, custody history, timestamps, user identifiers, and integrity hashes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
