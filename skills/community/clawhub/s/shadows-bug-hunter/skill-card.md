## Description: <br>
Structured debugging with 4 techniques: Log Injection, Screenshot Analysis, Manual Trace, and Test-Driven Fix for errors, broken UI, regressions, and runtime issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NakedoShadow](https://clawhub.ai/user/NakedoShadow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to triage bugs, choose an investigation technique, apply focused fixes, and verify that regressions and debug artifacts are cleared. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may edit repository files while debugging. <br>
Mitigation: Review generated diffs before committing and confirm that injected debug artifacts have been removed. <br>
Risk: Project test suites can execute arbitrary repository code. <br>
Mitigation: Use a sandbox when applying the skill to unfamiliar or untrusted codebases. <br>


## Reference(s): <br>
- [Shadows Bug Hunter Skill Page](https://clawhub.ai/NakedoShadow/shadows-bug-hunter) <br>
- [Publisher Profile](https://clawhub.ai/user/NakedoShadow) <br>
- [ClawHub Homepage](https://clawhub.ai/NakedoShadow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown bug report with root cause, fix, and verification sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file and line references, test results, and cleanup confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
