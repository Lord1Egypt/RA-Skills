## Description: <br>
Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fedrov2025](https://clawhub.ai/user/fedrov2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to review unfamiliar agent skills before installation, checking source trust, file behavior, permissions, and security red flags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release has no server-resolved GitHub import provenance, so origin cannot be verified from provenance evidence. <br>
Mitigation: Treat the ClawHub publisher profile as the available ownership signal and verify the publisher before relying on the skill for final security decisions. <br>
Risk: The skill includes example GitHub curl commands that fetch repository metadata and files. <br>
Mitigation: Run the example commands only against repositories intentionally selected for review and inspect fetched content before using it in installation decisions. <br>
Risk: The skill is a checklist and can miss context-specific or newly emerging threats. <br>
Mitigation: Use the generated vetting report as a review aid and apply human judgment for high-risk skills, credentials, privileged access, or system changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fedrov2025/skill-vetter-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/fedrov2025) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown checklist and vetting report template with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-readable security review guidance rather than executable artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
