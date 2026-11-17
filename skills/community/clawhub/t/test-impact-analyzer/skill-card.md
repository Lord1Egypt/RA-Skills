## Description:

Determine which tests need to run for a given code change: trace file dependencies, map source-to-test relationships, identify untested changes, and prioritize test execution order for faster CI feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to identify which tests are affected by code changes, map source files to tests, find untested paths, and generate a prioritized test execution plan for faster CI feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects repository paths, imports, test files, and recent git history.

Mitigation: Use it only in repositories where that inspection is acceptable, and review generated test plans before acting on them.

Risk: The CI example includes an unpinned npx Jest invocation that could trigger implicit package resolution.

Mitigation: Install locked dependencies first and invoke a local Jest binary or an explicitly pinned command in CI.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, optional JSON-shaped output examples, and CI configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs affected test paths, source-to-test mappings, untested file summaries, recommended execution phases, and test runner commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
