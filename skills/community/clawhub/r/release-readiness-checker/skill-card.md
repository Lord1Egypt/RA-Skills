## Description: <br>
Pre-release checklist for shipping software -- verify tests pass, changelog updated, version bumped, no debug code, dependencies clean, docs current, no secrets committed, CI green. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to audit software projects before tagging or shipping a release. It helps produce go/no-go readiness reports, manual checklists, and comparisons against a previous tagged release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is an advisory release checklist and should not be treated as the sole approval gate for a release. <br>
Mitigation: Run the project's actual test suite and CI separately before approving or tagging a release. <br>
Risk: Secret-scan matches may include sensitive values or false positives. <br>
Mitigation: Review findings carefully before sharing reports and redact any sensitive values. <br>
Risk: Some checks use networked npm or GitHub CLI operations that may rely on local credentials. <br>
Mitigation: Run those checks in an environment where npm and GitHub CLI authentication are expected and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/release-readiness-checker) <br>
- [Publisher profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Human-readable text, Markdown reports and checklists, JSON readiness summaries, shell command snippets, and CI configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can report GO, CAUTION, or NO-GO outcomes and uses exit codes 0, 1, and 2 for CI integration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
