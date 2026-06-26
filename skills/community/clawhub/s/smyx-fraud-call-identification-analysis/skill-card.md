## Description: <br>
Analyzes incoming call content for multi-dimensional fraud risk, identifies scam scripts, assesses risk levels, and generates an Anti-Fraud Guardian analysis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and security teams use this skill to analyze call recordings, URLs, or transcripts for fraud indicators and receive structured anti-fraud findings, risk levels, recommendations, and report links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Call content, local media files, or URLs may be sent to the publisher's cloud service. <br>
Mitigation: Use only when cloud processing is acceptable and ask the publisher to document data retention and deletion practices. <br>
Risk: Reports may be linked to a persistent local identity, with local token or SQLite storage not fully documented in the evidence. <br>
Mitigation: Review identity and local storage behavior before deployment, especially on shared or regulated systems. <br>
Risk: The security summary flags mismatched media-handling behavior and video-oriented code in a fraud-call skill. <br>
Mitigation: Confirm supported input types and operational scope before installation or production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fraud-call-identification-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, structured text reports, report links, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analysis may send call content, local media files, or URLs to the publisher's cloud service and may associate reports with a persistent local identity.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
