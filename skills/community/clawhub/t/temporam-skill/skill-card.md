## Description: <br>
Provides temporary email receiving functionality using the Temporam API, including temporary address generation, email listing, email content retrieval, and latest-email polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shulkme](https://clawhub.ai/user/shulkme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and automation agents use this skill to create temporary inboxes, inspect received messages, and retrieve verification emails through the Temporam API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime needs a Temporam API key to call the external service. <br>
Mitigation: Provide the key through TEMPORAM_API_KEY, avoid logging it, and install only where access to that credential is acceptable. <br>
Risk: Retrieved email contents, verification links, and codes may contain sensitive or untrusted data. <br>
Mitigation: Use temporary inboxes under the user's control, avoid sharing retrieved content, and treat links or codes as sensitive before acting on them. <br>


## Reference(s): <br>
- [Temporam API Reference](https://www.temporam.com/docs/api-reference) <br>
- [ClawHub Skill Page](https://clawhub.ai/shulkme/temporam-skill) <br>
- [Project Homepage](https://github.com/shulkme/temporam-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration] <br>
**Output Format:** [JSON-like tool results and text strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TEMPORAM_API_KEY; returned email contents and verification links should be treated as sensitive untrusted data.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
