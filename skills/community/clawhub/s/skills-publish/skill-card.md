## Description: <br>
Publish an OpenClaw skill to ClawHub with release checks, version metadata, and command generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fwwdn](https://clawhub.ai/user/fwwdn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to validate OpenClaw skill release inputs, prepare ClawHub publish metadata, and generate a reviewed publish command before upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A publish command could target the wrong skill folder, slug, display name, version, changelog, tags, or ClawHub account. <br>
Mitigation: Verify the target folder, release inputs, and active clawhub whoami account before approving any publish command. <br>
Risk: CLI authentication tokens could be exposed if the agent is asked to handle login details unnecessarily. <br>
Mitigation: Avoid giving the agent tokens unless local CLI authentication handling is explicitly required. <br>
Risk: Local checks cannot prove ClawHub authentication or server-side publish success before execution. <br>
Mitigation: Treat local readiness checks as preflight validation and verify the published listing after any confirmed upload. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/fwwdn/skills-publish) <br>
- [Publish Flow](references/publish-flow.md) <br>
- [Release Checklist](references/release-checklist.md) <br>
- [Local Release Checklist](references/checklist.md) <br>
- [Common Errors](references/common-errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and release-check summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a generated clawhub publish command after release inputs are reviewed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
