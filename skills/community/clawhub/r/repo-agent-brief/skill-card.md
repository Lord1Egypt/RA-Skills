## Description:

Generates concise, safety-aware repository orientation briefs before coding-agent work, reviews, handoffs, PR analysis, unfamiliar repository edits, or diff-aware branch handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[builtbyecho](https://clawhub.ai/user/builtbyecho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to gather repository orientation before edits, reviews, handoffs, pull request analysis, or safety-sensitive changes. It helps identify high-signal context files, stack and command hints, repository structure, and obvious risky-instruction or secret-pattern signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run an unpinned third-party npm package inside repositories that may contain sensitive code or configuration.

Mitigation: Use a pinned, reviewed version of @builtbyecho/repo-agent-brief and run it with minimal repository credentials.

Risk: Generated briefs may include snippets from repository context files.

Mitigation: Review generated briefs before sharing them and use --no-snippets when public or broad distribution is expected.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands; JSON is available when the underlying package is run with --format json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write repository brief files such as AGENT_BRIEF.md, AGENT_HANDOFF.md, agent-brief.json, or .agent-brief bundle files depending on the selected command.]

## Skill Version(s):

0.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
