## Description: <br>
Publishes workspace skills to GitHub and ClawHub using the user's configured local publishing workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spikesubingrui-design](https://clawhub.ai/user/spikesubingrui-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers maintaining OpenClaw workspace skills use this skill to publish approved skill updates to GitHub and ClawHub, including release version, slug, and repository publishing steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to publish files to GitHub and ClawHub using logged-in local accounts. <br>
Mitigation: Require fresh user confirmation before any non-dry-run publish command, and confirm the target skill path, GitHub visibility, slug, version bump, and included files. <br>
Risk: A mistaken target path, slug, or version can publish the wrong skill or overwrite expected release intent. <br>
Mitigation: Run the publishing workflow with --dry-run first and review the planned repository, ClawHub slug, and version before proceeding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spikesubingrui-design/skill-dual-publish) <br>
- [Publisher profile](https://clawhub.ai/user/spikesubingrui-design) <br>
- [Homepage](https://github.com/spikesubingrui-design/skill-dual-publish) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to run a local publishing script that may create or update GitHub and ClawHub releases.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
