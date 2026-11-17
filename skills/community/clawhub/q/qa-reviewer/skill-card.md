## Description:

Provides QA guidance, local code review checks, test-running scripts, and report templates for C++, Python, and JavaScript projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelpang](https://clawhub.ai/user/samuelpang)

### License/Terms of Use:

MIT

## Use Case:

Developers and QA engineers use this skill to review project code, run local test suites, track issues, and create QA reports during development and acceptance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's QA guidance and generated report text are primarily Chinese-language.

Mitigation: Install it only where Chinese-language QA guidance is acceptable, or translate generated reports before sharing them with teams that require another language.

Risk: The local scripts write markdown report files and may create test build directories in the target project.

Mitigation: Run the scripts against the intended project directory, preferably on a clean branch or disposable workspace, and review generated files before committing them.

Risk: The test runner can execute project-defined CMake or pytest behavior.

Mitigation: Review the target project's test configuration before invoking run_tests.sh and use an isolated environment when project tests are not yet trusted.

## Reference(s):

- [Skill documentation](SKILL.md)
- [Workflow guide](docs/workflow.md)
- [QA checklist](docs/checklist.md)
- [QA best practices](docs/best_practices.md)
- [Code review report template](templates/code_review.md)
- [Test report template](templates/test_report.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown reports, checklists, report templates, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local scripts may create CODE_REVIEW_*.md, TEST_RESULT_*.md, and test build directories in the target project.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
