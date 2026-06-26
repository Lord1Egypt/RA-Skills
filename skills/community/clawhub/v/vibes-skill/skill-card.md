## Description: <br>
Cultural intelligence — track albums, podcasts, shows, films, and YouTube channels that shaped how you think. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilyabelikin](https://clawhub.ai/user/ilyabelikin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to keep a local, searchable record of meaningful albums, podcasts, shows, films, and YouTube channels, including ratings, notes, tags, and social taste links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal culture notes, ratings, and social taste links in workspace files. <br>
Mitigation: Keep the workspace private, avoid recording sensitive relationships or preferences unless intended, and review mind/vibes/ before sharing or committing files. <br>
Risk: The skill can suggest recurring heartbeat or cron checks that resurface personal notes. <br>
Mitigation: Enable recurring checks only after explicit user approval, and disable them if repeated prompts over personal notes are not wanted. <br>
Risk: The skill includes an update path that replaces SKILL.md from a remote URL. <br>
Mitigation: Manually review the downloaded file and diff before replacing SKILL.md, then scan the updated skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilyabelikin/vibes-skill) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and conversational guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and searches local workspace files under mind/vibes/; may optionally reference images when enabled in vibesconfig.yml.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
