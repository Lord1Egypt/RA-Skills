## Description: <br>
Personal X/Twitter social media manager for crafting, reviewing, and optimizing posts, threads, replies, DMs, content strategy, engagement, growth, scheduling, and profile optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rabden](https://clawhub.ai/user/rabden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, founders, and professionals use this skill to plan X/Twitter strategy, draft posts and replies, analyze engagement, manage outreach, and keep a personalized content memory. It can also operate twitter-cli after explicit approval for account actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post, reply, DM, delete, like, follow, or schedule actions through an authenticated X/Twitter account. <br>
Mitigation: Require fresh explicit approval for every account action and review the final text, character count, target account, and command before execution. <br>
Risk: The skill depends on account-level authentication through twitter-cli, browser session state, or TWITTER_AUTH_TOKEN and TWITTER_CT0. <br>
Mitigation: Preinstall and review uv and twitter-cli yourself, confirm which X account is authenticated, and avoid exposing credentials outside the local agent environment. <br>
Risk: Persistent profile, memory, and real-replies archives can contain personal writing patterns, goals, performance data, and social graph details. <br>
Mitigation: Review generated strategy files periodically, remove sensitive entries, and purge the memory and reply archive when the skill is no longer needed. <br>
Risk: First-run setup may install CLI tooling and create or update local agent/sub-agent configuration. <br>
Mitigation: Review proposed installs and local file changes before allowing setup to proceed, especially in shared or production workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rabden/x-social-manager-dist) <br>
- [Publisher profile](https://clawhub.ai/user/rabden) <br>
- [Declared source repository](https://github.com/rabden/X-twitter-social-manager-skill) <br>
- [README](README.md) <br>
- [Twitter CLI Reference](references/cli-reference.md) <br>
- [Content Strategy Reference](references/content-strategy.md) <br>
- [Hook Library](references/hook-library.md) <br>
- [X Algorithm Playbook](references/algorithm-playbook.md) <br>
- [Voice Anti-Patterns](references/voice-anti-patterns.md) <br>
- [Sub-Agent Definitions](references/subagent-definitions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with optional shell commands and local file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce drafts, reply cards, content plans, DM templates, research summaries, account analysis, and proposed CLI actions for user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
