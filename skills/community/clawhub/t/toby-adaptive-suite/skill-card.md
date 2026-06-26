## Description: <br>
A continuously adaptive skill suite that empowers Clawdbot to act as a versatile coder, business analyst, project manager, web developer, data analyst, and NAS metadata scraper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use Adaptive-Suite for coding help, business analysis, project management, web and data development, resource discovery, and read-only NAS metadata-scraping support adapted to project context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a third-party SkillBoss API key and routes work through an external AI hub. <br>
Mitigation: Use a limited SkillBoss API key and require explicit approval before sending prompts, project files, filenames, directory structure, or user-context data to external services. <br>
Risk: The skill can collect NAS file names, metadata, and directory structure. <br>
Mitigation: Keep NAS scans read-only, avoid broad scans, and confirm scan scope before collecting or sharing metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-adaptive-suite) <br>
- [MOLT skills documentation](https://docs.molt.bot/tools/skills) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss API Hub endpoint](https://api.skillboss.co/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API-backed recommendations and read-only NAS metadata scanning workflows; review outputs before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
