## Description:

Detects a Radxa board, maps it to the correct product series, manages a local Radxa documentation mirror, and helps answer board-specific questions from offline documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xzl01](https://clawhub.ai/user/xzl01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to identify Radxa hardware, deploy or update a local documentation mirror when requested, and query the right board-specific documentation before coding, debugging, or hardware operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deploy and update workflow can run code from an external MDMaker repository.

Mitigation: Review the MDMaker repository, pin a trusted commit before deployment or update, run it in a sandbox or low-privilege account without sensitive credentials, and avoid updates unless the upstream code and package path are trusted.

## Reference(s):

- [Device Series Map](references/device-series-map.md)
- [MDMaker repository](https://github.com/ZIFENG278/MDMaker.git)
- [Radxa documentation source](https://github.com/radxa-docs/docs.git)
- [Radxa documentation GitCode mirror](https://gitcode.com/radxa-docs/docs.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local file path citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should distinguish local-documentation findings from model-mapping inferences.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
