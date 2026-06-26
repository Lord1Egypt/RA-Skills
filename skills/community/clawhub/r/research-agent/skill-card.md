## Description: <br>
Conduct open-ended research on a topic, building a living markdown document. Supports interactive and deep research modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and agent users use this skill to investigate topics, compare approaches, maintain living markdown research notes, and optionally run deeper asynchronous research through Parallel AI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts and findings are saved under the OpenClaw workspace, and deep research content may be sent to Parallel AI. <br>
Mitigation: Use the skill only for information you are comfortable storing in that workspace and sharing with Parallel AI during deep research. <br>
Risk: Setup guidance can expose PARALLEL_API_KEY broadly if the key is exported into every shell. <br>
Mitigation: Store the key in a protected secrets file, restrict file permissions, and avoid broad shell export unless that exposure is acceptable. <br>
Risk: Optional setup includes curl-to-shell installation and symlinking helper scripts into PATH. <br>
Mitigation: Prefer verified or package-manager installation methods where possible and inspect helper scripts before symlinking them. <br>
Risk: Cron auto-checks can continue polling or deliver results unexpectedly if scheduled for the wrong task. <br>
Mitigation: Enable auto-checks only for runs you started and verify scheduled times and task identifiers before creating cron jobs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/BrennerSpear/research-agent) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [uv Installer](https://astral.sh/uv/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research documents with inline shell commands and optional PDF exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates prompt.md, research.md, optional research.pdf, and related research-folder files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
