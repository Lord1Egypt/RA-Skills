## Description:

Generates deterministic lesson-plan skeletons from curriculum maps and checks existing plans for missing coverage, sources, stages, and time labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT

## Use Case:

Teachers and curriculum teams use it to turn a school-provided curriculum map into a structured lesson-plan skeleton, then check an existing plan for missing knowledge points, required stages, sources, and time labels. It also supports repeatable structure checks in batch workflows or CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned npm installation may retrieve a release different from the reviewed artifact.

Mitigation: Use a reviewed, fixed release and preview the installation with --dry-run.

Risk: A passing coverage check does not validate the sum of lesson-stage durations.

Mitigation: Manually confirm that stage times add up to periods multiplied by minutes per period.

Risk: Installation may replace customized files in an existing skill directory.

Mitigation: Select the intended agent or directory and back up customized skill files before installing.

## Reference(s):

- [Curriculum map and configuration format](references/map-format.md)
- [Lesson-plan and check-report format](references/plan-format.md)
- [Copyright and use boundaries](references/copyright.md)
- [Project homepage](https://github.com/YottaMeta/yotta-lesson)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-lesson)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown lesson-plan skeletons and JSON lesson plans or coverage-check reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Repeatable for the same inputs; plan generation allocates stage times to the configured total.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
