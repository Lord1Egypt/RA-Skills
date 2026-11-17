## Description:

Provides agent-runnable Node.js commands for searching public Xiaohongshu notes, fetching note details and comments, collecting note comments, and monitoring public creator posts for content research and marketing analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content teams, and analysts use this skill to collect structured public Xiaohongshu data for keyword research, competitive monitoring, creator review, trend tracking, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GUAIKEI_API_TOKEN and Xiaohongshu keywords or links may be sent to guaikei.com during use.

Mitigation: Use the skill only when that data transfer is acceptable, keep the token secret, and rotate it if exposure is suspected.

Risk: Target links, query terms, or command output may be retained in local logs.

Mitigation: Inspect and delete the logs directory after sensitive research, and avoid sharing raw command output when it contains confidential targets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-schedule-track)
- [GUAIKEI API service](https://www.guaikei.com)
- [Options and usage reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; executed commands return structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN for live API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package.json report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
