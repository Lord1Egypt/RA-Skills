## Description: <br>
Improves a skill's public listing before publish by tightening title, description, tags, changelog, and scan-friendly packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyoiii](https://clawhub.ai/user/kyoiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to review ClawHub skill listings before publishing or updating them, focusing on trust signals, discoverability, and small packaging improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flagged broad repository diff sharing with configured reviewer CLIs as requiring user review. <br>
Mitigation: Install only when comfortable sharing repository diffs with configured reviewers, prefer running without full-access modes, disable fallback reviewers when not needed, and avoid repositories containing secrets or private code. <br>


## Reference(s): <br>
- [Review Notes](references/review-notes.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/kyoiii/skill-listing-polisher) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include findings grouped by trust, discoverability, and the smallest recommended edit.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
