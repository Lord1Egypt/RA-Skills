## Description:

Xhs Expert helps agents search Xiaohongshu notes, collect note and comment data, manage login state, and perform like, collect, comment, follow, and batch engagement actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mieming1985](https://clawhub.ai/user/mieming1985)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators and agents use this skill to research Xiaohongshu content, collect local datasets, check account state, and perform reviewed engagement actions on selected notes or users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform real account-changing actions, including likes, collects, comments, follows, and batch engagement.

Mitigation: Require explicit review of every target and action before execution, keep batch sizes small, and avoid bulk engagement unless the operator has manually approved the full scope.

Risk: The skill stores login material and browser profile data locally.

Mitigation: Treat cookie and profile files as sensitive credentials, restrict local access, use an account dedicated to this workflow, and rotate or revoke sessions if files may have been exposed.

Risk: The skill can scrape and save Xiaohongshu content and comments.

Mitigation: Collect only the minimum data needed, protect exported JSON files, and review platform terms and privacy obligations before sharing or reusing collected data.

Risk: The skill includes browser stealth behavior that can hide automation signals.

Mitigation: Use automation only where permitted, avoid bypassing platform safeguards, and expect platform enforcement or account restrictions if automated behavior violates service rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mieming1985/skills/xhs-expert)
- [Xiaohongshu](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, JSON files, shell commands, configuration guidance]

**Output Format:** [CLI text, JSON exports, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local search result JSON and uses local browser profile and cookie files.]

## Skill Version(s):

1.0.0 (source: release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
