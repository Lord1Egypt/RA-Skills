## Description:

X Deep Miner is a scaffold for collecting high-engagement X/Twitter posts in AI, U.S. equities, and lifestyle topics and preparing Chinese-language Obsidian-style Markdown notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forvendettaw](https://clawhub.ai/user/forvendettaw)

### License/Terms of Use:


## Use Case:

Developers and knowledge workers use this skill to organize manually collected or browser-assisted X/Twitter posts into categorized Obsidian Markdown notes for personal knowledge bases and daily intelligence briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested cron entry can create persistent hourly execution.

Mitigation: Install the cron job only when persistent scanning is intended, use absolute paths, restrict project directory permissions, and document the removal command before deployment.

Risk: The implementation is mostly unfinished and may require manual or browser-assisted collection before useful notes are produced.

Mitigation: Run the test or status command first, confirm the collection workflow, and review generated notes before relying on them for briefings or archives.

## Reference(s):

- [X-Deep-Miner references](references/references.md)
- [X Explore](https://x.com/explore)
- [X Home](https://x.com/home)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown files and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates categorized Obsidian-style notes under an obsidian-output directory when content is available.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
