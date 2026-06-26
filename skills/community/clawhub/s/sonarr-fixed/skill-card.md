## Description: <br>
Search and add TV shows to Sonarr with monitor options and search-on-add support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frannunpal](https://clawhub.ai/user/frannunpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and automation agents use this skill to search Sonarr, check library status, add TV shows with a selected or default quality profile, and remove shows when confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remove shows from a Sonarr library, and --delete-files can delete associated media files through Sonarr. <br>
Mitigation: Confirm every remove action before running it and treat --delete-files as destructive. <br>
Risk: The skill uses a Sonarr API key to change the connected Sonarr instance. <br>
Mitigation: Install only when agent-driven Sonarr management is intended and limit credentials to the intended Sonarr instance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/frannunpal/sonarr-fixed) <br>
- [Original Sonarr skill](https://clawhub.com/jordyvandomselaar/sonarr) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and JSON from shell commands, with Markdown guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Sonarr URL and API key via config file or environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
