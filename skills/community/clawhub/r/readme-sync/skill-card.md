## Description: <br>
README Sync helps agents read relevant README sections before project work and propose confirmed README updates afterward. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyqfxy](https://clawhub.ai/user/zyqfxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to keep project README files aligned with coding work. It guides agents to read only relevant README context, cache notable changes, and sync approved updates after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: README summaries or pending update state may contain sensitive project details if the user records them there. <br>
Mitigation: Review proposed README and .readme_pending.json content before syncing, avoid adding secrets, and clear pending state when it should not persist. <br>
Risk: The init, auto-init, and sync workflows can modify README-related files in the local project. <br>
Mitigation: Run preview or pending-review commands first and require user confirmation before applying README changes. <br>


## Reference(s): <br>
- [README template](references/readme_template.md) <br>
- [ClawHub skill page](https://clawhub.ai/zyqfxy/readme-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prose with shell command snippets and local README updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update README.md and .readme_pending.json after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
