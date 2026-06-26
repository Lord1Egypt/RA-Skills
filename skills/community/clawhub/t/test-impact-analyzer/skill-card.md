## Description: <br>
Determine which tests need to run for a given code change by tracing file dependencies, mapping source-to-test relationships, identifying untested changes, and prioritizing test execution order for faster CI feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide which tests to run for a code change, find source-to-test mappings, identify untested files, and generate targeted CI test commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated test-runner commands may be incorrect or risky in repositories with unusual or untrusted file names. <br>
Mitigation: Review generated commands before executing them in CI and quote or sanitize file paths in automation. <br>
Risk: Heuristic file-name and grep-based import analysis can miss affected tests or include unrelated tests. <br>
Mitigation: Treat the plan as a targeted starting point and keep full-suite testing for merge, release, or high-risk changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON or path-list output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces affected-test summaries, source-to-test maps, untested-file reports, prioritized execution plans, and test-runner commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
