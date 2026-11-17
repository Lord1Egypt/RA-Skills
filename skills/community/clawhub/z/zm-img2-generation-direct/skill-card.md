## Description:

ZM IMG2 直接生图执行用于通过 happy/gpt-image-2 执行文生图和参考图生图，并保留输入、输出、日志和结果 JSON 作为正式视觉生产证据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and visual-production operators use this skill to generate text-to-image and reference-image outputs through a configured Happy OpenAI-compatible image provider while retaining review evidence for acceptance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags under-disclosed task-controlled shell execution in queue inputs.

Mitigation: Install only for trusted task submitters, avoid command and mock_command fields for normal use, and run the skill in a tightly scoped sandbox.

Risk: Security evidence flags broad local file and network handling.

Mitigation: Restrict provider configuration to approved endpoints, scope state and output directories, and treat prompts, input paths, logs, and generated artifacts as retained local records.

Risk: Security evidence gives a suspicious verdict and says the skill needs review before installation.

Mitigation: Review the skill before deployment and accept generated images only when result evidence proves ok status, provider, model, mode, input images, and output bytes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-img2-generation-direct)
- [AI readiness checklist](artifact/checklists/ai_readiness_checklist.md)
- [Minimum required fields template](artifact/templates/minimum_required_fields.md)
- [Subagent execution prompt template](artifact/templates/subagent_execution_prompt.md)

## Skill Output:

**Output Type(s):** [Images, JSON, Logs, Shell commands, Guidance]

**Output Format:** [Generated image files with result JSON, request records, state files, and stdout/stderr logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the configured happy/gpt-image-2 provider, supports text-to-image and up to five reference images per task, and includes bounded batch and queue wrappers.]

## Skill Version(s):

0.1.0 (source: server release metadata and target metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
