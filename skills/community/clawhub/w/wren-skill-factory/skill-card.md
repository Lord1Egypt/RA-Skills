## Description: <br>
Builds and publishes OpenClaw skills from recurring pain points by scanning .learnings entries, scaffolding skill directories, and publishing selected skills to ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wrentheai](https://clawhub.ai/user/wrentheai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Skill Factory to turn recurring .learnings pain points into reusable OpenClaw skills. It supports scanning for candidates, scaffolding from a description or error entry, and packaging a skill for publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publish command can upload local skill contents under an authenticated ClawHub account. <br>
Mitigation: Review package contents for secrets or private logic and confirm the ClawHub account, slug, and destination before publishing. <br>
Risk: Shell-string command construction can be unsafe when used with untrusted skill directories or metadata. <br>
Mitigation: Avoid untrusted skill directories and SKILL.md metadata until command execution is changed to argument-array execution. <br>
Risk: Generated skill scaffolds may encode incomplete or incorrect fixes from .learnings entries. <br>
Mitigation: Review, test, and scan generated skills before deployment or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wrentheai/wren-skill-factory) <br>
- [Publisher profile](https://clawhub.ai/user/wrentheai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with CLI commands and generated skill scaffold files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create skill directories and can publish skill contents through an authenticated ClawHub CLI session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
