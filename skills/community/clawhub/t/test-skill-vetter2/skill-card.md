## Description: <br>
Security-first skill vetting for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xavi296](https://clawhub.ai/user/xavi296) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to review third-party AI agent skills before installation by checking source, file contents, permissions, red flags, and risk level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example commands in the skill may contact GitHub when used during review. <br>
Mitigation: Run network commands only when the reviewed source is expected to be GitHub-hosted and the network destination is acceptable. <br>
Risk: Reviewing an unknown skill can require reading files from that skill. <br>
Mitigation: Limit file access to the skill being reviewed and avoid granting credential or broader local access unless the review specifically requires it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xavi296/test-skill-vetter2) <br>
- [Publisher profile](https://clawhub.ai/user/xavi296) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with checklist items and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a skill vetting report that records source, author, reviewed files, red flags, permissions, risk level, verdict, and notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
