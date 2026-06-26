## Description: <br>
Smart File Organizer Pro helps organize local files with preset modes for type-based sorting, date archiving, duplicate handling, progress display, operation history, and undo support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shianaixuexi-cell](https://clawhub.ai/user/shianaixuexi-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect local directories and organize files into predictable folders by type, date, and duplicate status. It is best suited for controlled local cleanup workflows that start with preview mode and backups enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move, rename, archive, and deduplicate local files, which may make files hard to find or recover if run on a broad directory. <br>
Mitigation: Start with --preview on a small test folder, keep backups enabled, and review planned changes before running on important files. <br>
Risk: Duplicate handling can remove or relocate files if configured aggressively. <br>
Mitigation: Use conservative duplicate settings first and avoid delete behavior unless the user has verified the matches and accepts the risk. <br>
Risk: Organizing sensitive or system directories can disrupt workflows or expose private file names in reports. <br>
Mitigation: Avoid broad, sensitive, hidden, and system directories until the behavior is understood; use safe mode and explicit include or exclude filters where possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shianaixuexi-cell/smart-file-organizer-pro) <br>
- [README](README.md) <br>
- [Default Configuration](config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and local script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce file analysis summaries, operation reports, history entries, backup records, and undo guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
