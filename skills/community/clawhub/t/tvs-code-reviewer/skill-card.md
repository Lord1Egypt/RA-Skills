## Description: <br>
A strict, evidence-driven code review skill that requires a clear review scope, checks code through a fixed review checklist, and reports confirmed issues with severity, location, evidence, impact, confidence, and trigger conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inksnowhailong](https://clawhub.ai/user/inksnowhailong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run scoped, evidence-based code reviews of files, diffs, pull requests, commits, snippets, or failure logs. It is designed to surface real defects, validation gaps, and limited out-of-scope observations without rewriting the reviewed code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews only the scope supplied by the user, so incomplete inputs can lead to incomplete findings. <br>
Mitigation: Provide the exact files, diff, pull request, commit range, snippet, or logs that should be reviewed. <br>
Risk: Code review findings can be incorrect or lack runtime confirmation when supporting evidence is limited. <br>
Mitigation: Check reported locations and run the suggested minimal validation before acting on findings. <br>
Risk: The skill needs access to the files, diffs, logs, or snippets selected for review. <br>
Mitigation: Share only the intended review scope and avoid including secrets or unrelated sensitive data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/inksnowhailong/tvs-code-reviewer) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/inksnowhailong) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown review findings with severity headings, locations, confidence, evidence, impact, trigger conditions, validation gaps, and optional out-of-scope observations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not provide code fixes; asks for a concrete review scope before reviewing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
