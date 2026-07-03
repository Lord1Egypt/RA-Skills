## Description: <br>
ZM IMG2 直接生图执行。用于通过 happy/gpt-image-2 执行文生图和参考图生图，保留输入、输出、日志和结果 JSON，作为正式视觉生产证据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content production agents use this skill to run prompt-only or reference-based image generation through the configured Happy provider and retain image paths, result JSON, logs, and proof fields for visual acceptance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The queue can run arbitrary task-supplied shell commands through command or mock_command paths. <br>
Mitigation: Install and run only in a sandbox or trusted workspace unless those execution paths are removed or strongly gated. <br>
Risk: Prompts, reference image paths, logs, result files, and reference images may be stored locally or sent to the configured Happy image provider. <br>
Mitigation: Avoid sensitive prompts and images unless provider use is approved, and review local artifacts before sharing or retaining them. <br>
Risk: The server security verdict is suspicious and requires human review before installation. <br>
Mitigation: Review the skill, scan it before deployment, and verify result JSON proof fields before accepting generated images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-img2-generation-direct) <br>
- [AI readiness checklist](checklists/ai_readiness_checklist.md) <br>
- [Minimum required fields](templates/minimum_required_fields.md) <br>
- [Subagent execution prompt](templates/subagent_execution_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; runtime artifacts are PNG images, JSON result files, and logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, node, and a configured Happy image provider; reference-image tasks support up to five input images.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
