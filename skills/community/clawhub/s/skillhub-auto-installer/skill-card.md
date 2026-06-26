## Description: <br>
Searches the Skillhub marketplace for available skills and returns read-only search results for agent users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiayao0810](https://clawhub.ai/user/jiayao0810) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search the Skillhub marketplace, review candidate skills, and decide which skills to inspect or install manually. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package presents itself as read-only search support, but server security evidence reports installer and local-audit scripts that can modify the agent environment. <br>
Mitigation: Use search.sh for read-only searching, and do not run install.sh or secure-install.sh unless the target skill has been reviewed and remote download plus workspace writes are acceptable. <br>
Risk: Manual installation guidance may lead users to install third-party skills without reviewing their behavior. <br>
Mitigation: Review each target skill before installation and run the documented security checks before executing any install command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiayao0810/skillhub-auto-installer) <br>
- [Skillhub Auto-Finder + SkillSentry integration guide](artifact/references/security-integration.md) <br>
- [Skillhub API endpoint](https://skills.volces.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown with shell command snippets and Skillhub search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a query string and optional result limit when invoking search.sh] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
