## Description: <br>
Social Ops coordinates role-based social media operations for scouting opportunities, researching trends, creating content, posting, responding, and analyzing performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dougbtv](https://clawhub.ai/user/dougbtv) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Agents and operators use this skill to run structured social presence workflows, including opportunity detection, content pipeline management, community engagement, publishing, and performance review. It is suited to intentional social operations where role boundaries, logs, and human-configured goals are important. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring social-media jobs can post, reply, and use account credentials with limited built-in approval controls. <br>
Mitigation: Enable scheduled jobs only for intended accounts, run the installer with --dry-run first, inspect each schedule and prompt, and add a manual approval step for posts, replies, subscriptions, and other account-facing actions. <br>
Risk: The skill can read local reference files selected through the social operations data directory. <br>
Mitigation: Keep SOCIAL_OPS_DATA_DIR isolated and keep Local-File-References small, explicit, and free of private or regulated material unless that use is intentional. <br>
Risk: Automated social engagement may create spam-like or off-brand behavior if role boundaries and operator goals are not maintained. <br>
Mitigation: Use the documented role constraints, goal files, logs, and cadence limits; review generated content and engagement actions against the operator's guardrails before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dougbtv/social-ops) <br>
- [Publisher profile](https://clawhub.ai/user/dougbtv) <br>
- [Configuration Guide](Guidance/CONFIGURATION-GUIDE.md) <br>
- [Role Input/Output Map](references/ROLE-IO-MAP.md) <br>
- [Cron Baseline](references/crons/InstallCrons.md) <br>
- [Local File References Template](references/LOCAL-FILE-REFERENCES-TEMPLATE.md) <br>
- [Social Strategy](assets/strategy/Social-Networking-Plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, role-specific social content artifacts, logs, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide scheduled social-media operations through OpenClaw cron jobs and platform-specific skills; account-facing actions should be reviewed according to operator policy.] <br>

## Skill Version(s): <br>
0.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
