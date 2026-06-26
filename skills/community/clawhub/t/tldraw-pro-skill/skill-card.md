## Description: <br>
Use when user requests diagrams, flowcharts, architecture charts, or visualizations, and generate .tldr JSON files that can be exported to PNG or SVG locally with @kitschpatrol/tldraw-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn natural-language requests into whiteboard-style architecture diagrams, flowcharts, sequence sketches, ML diagrams, ERDs, and UML-style class diagrams. It is suited for explainers, internal documentation, and iterative diagram drafting where .tldr source plus PNG or SVG exports are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently self-update from Git once every 24 hours. <br>
Mitigation: Disable or remove the silent git pull step for controlled environments, and pin reviewed skill versions before deployment. <br>
Risk: The skill may install a global npm CLI dependency if tldraw is missing. <br>
Mitigation: Install @kitschpatrol/tldraw-cli manually from a trusted source and use normal dependency review before enabling the skill. <br>
Risk: Vision self-checks may process confidential architecture or business diagrams. <br>
Mitigation: Skip vision self-checks or use an approved local/private vision model for sensitive diagrams. <br>


## Reference(s): <br>
- [Tldraw Skill on ClawHub](https://clawhub.ai/agents365-ai/tldraw-pro-skill) <br>
- [Project homepage](https://github.com/Agents365-ai/tldraw-skill) <br>
- [tldraw editor](https://tldraw.com) <br>
- [Agent Skills format](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with JSON file content and shell commands; generated artifacts are .tldr JSON plus PNG or SVG exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and tldraw CLI on PATH; optional vision self-check reads exported PNGs when a vision-capable model is available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
