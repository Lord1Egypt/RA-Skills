## Description: <br>
Scan Reddit for pain points in a product's niche, identify a real user complaint worth fixing, and prepare an approved patch or PR workflow for a target repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcnutt1414](https://clawhub.ai/user/mcnutt1414) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product engineers use this skill to turn Reddit feedback into a prioritized fix proposal and, after explicit approval, a local patch or pull request workflow for a configured repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write-enabled patch or PR mode can modify repository files, create commits, push branches, or open pull requests if approved. <br>
Mitigation: Keep analyze mode as the default, confirm the configured repoPath, and require explicit approval for the selected Reddit complaint, proposed fix, likely changed files, and tests before any write action. <br>
Risk: Scheduled runs or Slack notifications could send low-signal findings or route results to the wrong destination. <br>
Mitigation: Use analyze mode for scheduled runs unless deliberately reconfigured, and verify the Slack destination and cron schedule before enabling notifications. <br>
Risk: Reddit complaints may be weak, ambiguous, or not representative enough to justify a product change. <br>
Mitigation: Prefer current, specific complaints; document frequency, severity, fixability, and confidence; and stop with an analysis report when no credible complaint is found. <br>


## Reference(s): <br>
- [Reddit to PR on ClawHub](https://clawhub.ai/mcnutt1414/reddit-to-pr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration examples, shell commands, patch or PR guidance, and local run reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to analysis-only and requires explicit user approval before repository edits, commits, pushes, PR creation, or Slack notifications.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
