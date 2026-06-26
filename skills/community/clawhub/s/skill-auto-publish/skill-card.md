## Description: <br>
Safely publish an already-reviewed skill to ClawHub, verify the live registry state, and return a clear release report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choosenobody](https://clawhub.ai/user/choosenobody) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release operators use this skill to publish reviewed ClawHub skills, verify the live registry state, and return a clear release report with any blocking issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing can update public marketplace content. <br>
Mitigation: Before running publish commands, confirm the logged-in ClawHub account, slug, source path, version, changelog, and release review status. <br>
Risk: A successful publish command may not prove that the live page is correct or fully propagated. <br>
Mitigation: Verify the registry with clawhub inspect, check the public page when accessible, and report blocked or mismatched verification honestly. <br>


## Reference(s): <br>
- [Publish Checklist](references/publish-checklist.md) <br>
- [Verification Protocol](references/verification-protocol.md) <br>
- [Known Platform Limitations](references/archive/known-platform-limitations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown release report with status fields and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports publish status, registry verification, public page verification, URL, install command, issues, and next action.] <br>

## Skill Version(s): <br>
2.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
