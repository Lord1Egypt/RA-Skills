## Description: <br>
Enforces release discipline for AI agents and developers by requiring quality checks, cooldown review, feedback review, documentation checks, and release logging before publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyeuun97](https://clawhub.ai/user/gyeuun97) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release agents use this skill to review publish, deploy, version bump, and release requests before they proceed. It helps identify premature releases, missing documentation, lack of user feedback, cooldown violations, and contradictions with stated project principles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Release rationales, feedback summaries, or local release logs could include secrets, sensitive customer details, or private incident information. <br>
Mitigation: Keep sensitive data out of release rationale and feedback summaries, and review memory/release-log.md before sharing or publishing. <br>
Risk: The skill can challenge or block releases until checklist gates pass. <br>
Mitigation: Use human review for final release decisions and document any intentional override with the release reason. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gyeuun97/release-discipline) <br>
- [Publisher profile](https://clawhub.ai/user/gyeuun97) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown and plain-text release review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append approved, blocked, or warned release entries to memory/release-log.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
