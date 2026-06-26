## Description: <br>
Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review third-party skills before installation, checking source trust, file behavior, permission scope, and security red flags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Placeholder GitHub commands could be pointed at the wrong repository or skill path. <br>
Mitigation: Replace OWNER, REPO, and SKILL_NAME carefully and confirm the listing and version before reviewing results. <br>
Risk: A checklist-only review can miss behavior if not all skill files are inspected. <br>
Mitigation: Read every file in the candidate skill and compare observed behavior against the requested permissions and security guidance. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/asterisk622/xiaoding-skill-vetter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with checklist findings and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a skill vetting report covering source, author, version, files reviewed, red flags, permissions, risk level, verdict, and notes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
