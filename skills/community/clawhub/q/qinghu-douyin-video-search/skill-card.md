## Description:

Searches Douyin videos by keyword and returns video details and engagement metrics with optional sorting, duration, and publication-time filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to find Douyin videos by keyword and compare creators, publishing dates, and engagement for a specified search period.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to install or update external Node and qhkit tooling, including unpinned packages and possible persistent PATH changes.

Mitigation: Review and approve package installs, downloads, and shell configuration changes before execution; avoid persistent PATH changes unless needed.

Risk: The skill requires a Qinghu API token and makes paid searches whose cost can rise with result volume.

Mitigation: Configure the token securely, verify estimated credits, and obtain user approval before paid searches or large batches.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-douyin-video-search)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written findings with video previews; larger result sets as a table file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include video IDs, authors, titles, timestamps, download links, and engagement counts; paid calls report Qinghu credit usage.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
