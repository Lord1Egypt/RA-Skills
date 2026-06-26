## Description: <br>
Paperzilla CLI helps agents search, filter, and browse AI-curated academic papers by project through the Paperzilla command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pors](https://clawhub.ai/user/pors) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate the Paperzilla CLI from an agent workflow: log in, list projects, browse and filter research feeds, export JSON, and generate Atom feed URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill requires trusting Paperzilla, the installed pz binary, and the selected distribution channel. <br>
Mitigation: Install only from trusted Paperzilla channels and review install commands before execution, especially Linux commands that place a downloaded binary in the system path. <br>
Risk: Atom feed URLs may include embedded feed tokens that can grant access to the feed if shared. <br>
Mitigation: Treat generated Atom URLs as secrets, avoid sharing them, and revoke or regenerate tokens if a URL is exposed. <br>


## Reference(s): <br>
- [Paperzilla](https://paperzilla.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pz binary and an authenticated Paperzilla account; Atom feed URLs can include embedded tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
