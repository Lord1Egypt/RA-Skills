## Description:

这是我的测试32323

This skill is ready for commercial/non-commercial use.

## Publisher:

[yequanzheng](https://clawhub.ai/user/yequanzheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a compact GitHub CLI reference for checking pull request CI, listing workflow runs, inspecting failed runs, querying GitHub API fields, and producing JSON-filtered issue output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The GitHub CLI commands can use the installing user's existing GitHub authentication and access repositories that user is authorized to view.

Mitigation: Review commands before running them, specify the intended repository explicitly, and use least-privileged GitHub credentials when working across organizations or private repositories.

Risk: The skill metadata is vague, which can make the intended behavior harder to assess before installation.

Mitigation: Inspect the short artifact contents and confirm it is only a GitHub CLI reference before deploying it to agents.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
