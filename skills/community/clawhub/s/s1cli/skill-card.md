## Description: <br>
s1cli helps agents use the Stage1st (S1) forum CLI to log in, browse forums and threads, post or reply, search, check in, view profiles, and manage configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Geoion](https://clawhub.ai/user/Geoion) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill when helping users operate the Stage1st forum through the s1cli Python package, including browsing, searching, posting, replying, check-ins, profile lookup, and configuration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports account login and may involve local session files for a Stage1st account. <br>
Mitigation: Prefer interactive login, avoid passing passwords on the command line, and protect or remove ~/.config/s1cli/session.toml when finished. <br>
Risk: The skill can post, reply, and check in on behalf of a user. <br>
Mitigation: Require explicit user approval before any posting, replying, or check-in action. <br>
Risk: The skill depends on an external s1cli Python package. <br>
Mitigation: Verify the package source before installation and install only when the user intends to use Codex with a Stage1st account. <br>


## Reference(s): <br>
- [Complete s1cli command reference](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that authenticate to Stage1st or perform forum actions only after user approval.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
