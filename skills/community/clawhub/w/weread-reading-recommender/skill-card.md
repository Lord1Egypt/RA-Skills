## Description:

Use this skill when the user wants to export local WeRead records, normalize WeRead data, analyze reading preferences from WeRead history, or get book recommendations grounded in WeRead reading behavior and a current learning goal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cengsin](https://clawhub.ai/user/cengsin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to export and normalize their own local WeRead reading records, then generate reading-profile analysis and book recommendations from normalized reading history and an optional current learning goal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The export workflow uses a live WeRead session cookie.

Mitigation: Use a protected local cookie file or managed environment variable, avoid passing the cookie directly on the command line, and never include the cookie in skill files, logs, exported JSON, or responses.

Risk: Raw and normalized exports can contain detailed reading-history data.

Mitigation: Store exports in a private local directory, review or delete raw exports when finished, and use the normalized JSON for recommendation work whenever possible.

Risk: Refreshing data can contact WeRead endpoints and update local files.

Mitigation: Refresh only when explicitly requested and review generated files before sharing or reusing them outside the local workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cengsin/skills/weread-reading-recommender)
- [Data Schema](references/data-schema.md)
- [Privacy Model](references/privacy-model.md)
- [Recommendation Rubric](references/recommendation-rubric.md)
- [WeRead](https://weread.qq.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local JSON file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local raw and normalized JSON files when export or normalization commands are run.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
