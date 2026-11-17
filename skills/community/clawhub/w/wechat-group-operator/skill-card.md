## Description:

WeChat group operations automation for Windows desktop WeChat. Use when the user wants to run recurring group engagement workflows such as morning questions, afternoon follow-ups, and evening case posts in specified微信群, with content pools, posting history, and OpenClaw cron scheduling. Best for群运营、私域活跃、课程群维护、社群节奏 automation. Not for朋友圈 scraping or broad WeChat data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinhuadeng](https://clawhub.ai/user/jinhuadeng)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and community managers use this skill to prepare and run recurring WeChat group engagement posts for manually whitelisted groups. It supports scheduled morning questions, afternoon follow-ups, and evening case posts using maintained content pools and dry-run previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real WeChat group messages from the local desktop session.

Mitigation: Review and edit the group whitelist and content pools, run dry runs first, and enable cron only after manual sends behave as expected.

Risk: Live sends rely on an external desktop sender script outside this artifact.

Mitigation: Verify the sender script path is trusted and protected from modification before allowing real sends.

Risk: The posting history file is used at runtime to reduce repeats and may need initialization.

Mitigation: Create and review the post history file before scheduled execution so runs do not fail or repeat content unexpectedly.

## Reference(s):

- [Actions](references/actions.md)
- [Config](references/config.md)
- [Cron setup](references/cron-setup.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run mode previews intended posts; real sends can post to enabled WeChat groups through a local desktop sender.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
