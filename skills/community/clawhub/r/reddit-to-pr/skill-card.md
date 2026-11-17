## Description:

Scans Reddit for recent product pain points, selects an actionable complaint, and prepares an approval-gated fix proposal or patch/PR workflow for a target repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcnutt1414](https://clawhub.ai/user/mcnutt1414)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product engineers use this skill to turn public Reddit complaints into a prioritized fix proposal and, after explicit approval, a local patch or PR in a configured repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches public Reddit content and may use low-signal or ambiguous complaints as input.

Mitigation: Review the selected complaint, root-cause analysis, and confidence before approving any implementation work.

Risk: Patch and PR modes can modify a configured repository, commit, push, or open a pull request after approval.

Mitigation: Keep scheduled runs in analysis mode by default and require explicit approval for the selected fix before edits, commits, pushes, or PR creation.

Risk: Generated PR text includes an OpenClaw attribution footer.

Mitigation: Review PR text before publishing and adjust wording to match project contribution requirements.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown proposals, JSON run reports, configuration JSON, git commands, and code changes when explicitly approved.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to analysis-only; repository edits, commits, pushes, PR creation, and Slack notifications require the configured mode, available credentials, and explicit approval.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
