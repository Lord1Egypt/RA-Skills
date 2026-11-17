## Description:

Fetches a GitHub user's starred repositories through the GitHub API and generates a categorized Chinese Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blckrabbit](https://clawhub.ai/user/blckrabbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to analyze a GitHub user's starred repositories, group them by category and language, and produce a shareable Chinese Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub tokens can be supplied through command-line arguments.

Mitigation: Prefer unauthenticated use; if a token is needed, use a short-lived GitHub token with no permissions and avoid passing valuable PATs in command arguments.

Risk: The output path can overwrite writable files.

Mitigation: Keep output paths inside a dedicated reports folder and review the path before running the script.

Risk: The skill runs a local Python script and fetches public GitHub data over the network.

Mitigation: Install only after review, run it for intended GitHub usernames, and expect GitHub API availability and rate limits to affect results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blckrabbit/skills/yardor)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown report file with summary tables and categorized repository lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to the GitHub API and may optionally use a GitHub token for higher rate limits.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
