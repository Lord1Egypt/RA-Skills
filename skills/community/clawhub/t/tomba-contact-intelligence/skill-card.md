## Description: <br>
Use Tomba MCP tools for contact discovery, verification, enrichment, and company research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benemohamed](https://clawhub.ai/user/benemohamed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sales or research teams use this skill to guide Tomba-backed prospecting workflows, including contact discovery, email verification, lead enrichment, phone lookup, company research, and competitor analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Names, emails, phone numbers, LinkedIn URLs, and lead details may be sent to Tomba during contact intelligence workflows. <br>
Mitigation: Use the skill only when authorized to process the submitted contact data, and follow applicable privacy laws and platform terms. <br>
Risk: The skill requires Tomba API credentials for normal operation. <br>
Mitigation: Store Tomba API keys as secrets, restrict access to intended users, and rotate or revoke keys when access is no longer needed. <br>
Risk: Contact discovery results can mix verified data with inferred or lower-confidence findings. <br>
Mitigation: Present verification status and source inputs clearly, and avoid treating unverified contact data as confirmed. <br>


## Reference(s): <br>
- [Tomba Homepage](https://tomba.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/benemohamed/tomba-contact-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Concise Markdown or plain text summaries with verified and inferred data labeled.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source inputs, email verification status, ranked contact recommendations, and next lookup suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
