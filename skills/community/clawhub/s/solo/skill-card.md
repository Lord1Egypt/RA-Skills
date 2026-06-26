## Description: <br>
SOLO is an OpenClaw meta-agent framework for coordinating a kernel, an audit layer, and execution skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meta-evo-creator](https://clawhub.ai/user/meta-evo-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to organize an OpenClaw-based agent fleet with audit records, learning promotion guidance, and recurring review workflows. It is aimed at coordinating operational skills while preserving review boundaries between proposed changes and execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can maintain persistent audit state and cron-style operational records. <br>
Mitigation: Restrict writable paths to the intended audit and status directories, and review generated records regularly. <br>
Risk: The included upload workflow can send local Markdown or text content to an external IMA knowledge base using API credentials. <br>
Mitigation: Require explicit approval before any upload, scope credentials narrowly, and verify the selected file path and destination knowledge base before execution. <br>
Risk: Audit proposals may influence future skill behavior if accepted without review. <br>
Mitigation: Keep audit outputs advisory until a human reviewer approves any promoted rule, checklist, or SOP change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meta-evo-creator/solo) <br>
- [SOLO README](README.md) <br>
- [SOLO audit agent](agent-audit.md) <br>
- [Eval loop for self-improvement](references/eval-loop.md) <br>
- [Promotion guide](references/promotion-guide.md) <br>
- [Learning schema](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, status text, JSON status/audit records, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read audit inputs, write audit/status files, and invoke credentialed upload workflows when configured.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
