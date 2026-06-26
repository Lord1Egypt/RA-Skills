## Description: <br>
reddi.tech fork of git-summary. Get a quick summary of the current Git repository including status, recent commits, branches, and contributors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to quickly inspect and summarize a local Git repository's branch status, recent commits, remotes, uncommitted changes, and contributors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Git summaries can reveal private repository details such as remote URLs, branch names, commit messages, contributor names, and changed file paths. <br>
Mitigation: Review the generated summary before sharing it, and redact sensitive repository metadata or token-bearing URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/reddi-git-summary) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary based on local Git command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git and runs local read-only repository inspection commands; no outbound network access is required.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and changelog list 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
