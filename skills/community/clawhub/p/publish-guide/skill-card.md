## Description: <br>
Prepare and publish an OpenClaw AgentSkill to ClawHub, including pre-publish checks, publish execution, and post-publish verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ham-5on](https://clawhub.ai/user/ham-5on) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to prepare an AgentSkill directory for ClawHub release, run publication checks, execute the publish command, and verify the published skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to publish or update a public ClawHub skill under the active account. <br>
Mitigation: Review the target directory, authenticated account, slug, version, tags, and changelog before allowing the publish command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ham-5on/publish-guide) <br>
- [Publisher profile](https://clawhub.ai/user/ham-5on) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and checklist tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clawhub CLI for publish, inspect, search, login, and account verification commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
