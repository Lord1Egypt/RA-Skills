## Description: <br>
Publish and manage articles on Tilda website builder via browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vspandexe](https://clawhub.ai/user/vspandexe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and content teams use this skill to create, edit, and publish Tilda pages or article drafts through browser automation when a direct write API is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to a Tilda account that can publish live website changes. <br>
Mitigation: Use a dedicated or least-privileged Tilda account where possible and require confirmation of the exact project, page, destination, and content before saving or publishing. <br>
Risk: The skill stores the Tilda account password locally and may create session, screenshot, log, or selector-cache files during troubleshooting. <br>
Mitigation: Keep .env and session files out of source control and backups, and delete debug screenshots and logs after troubleshooting. <br>
Risk: The onboarding flow can install Playwright through npm or npx. <br>
Mitigation: Review and approve package installation commands explicitly before they run. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vspandexe/tilda-publisher) <br>
- [Publisher Profile](https://clawhub.ai/user/vspandexe) <br>
- [Tilda Login](https://tilda.cc/login/) <br>
- [Tilda Projects](https://tilda.cc/projects/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command snippets; publishing runs return status text and live URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local .env credentials, Playwright session state, debug screenshots, logs, and learned selector JSON when used as instructed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
