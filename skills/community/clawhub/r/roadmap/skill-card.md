## Description: <br>
Roadmap is a command-line product roadmap planner for timelines, milestones, feature tracking, priority scoring, dependency mapping, and progress visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, and automation agents use Roadmap to capture roadmap items, plans, progress notes, priorities, timelines, reports, and exports from a terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Roadmap entries are stored locally in plaintext and may be included in exports. <br>
Mitigation: Avoid entering passwords, API keys, or sensitive business details; review files under ~/.local/share/roadmap before sharing exports. <br>
Risk: The documentation claims ROADMAP_DIR can change the data directory, but the reviewed script hardcodes ~/.local/share/roadmap. <br>
Mitigation: Assume the default data directory unless the script is updated and re-reviewed; check the CLI status output before relying on a different location. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bytesagain1/roadmap) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration] <br>
**Output Format:** [Plain text CLI output with optional JSON, CSV, or TXT exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores roadmap log and export files under ~/.local/share/roadmap.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
