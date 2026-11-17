## Description:

RHSkill lets an OpenClaw agent call the RunningHub AI platform directly to run image, video, audio, and chained generation workflows with configurable output storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airix315](https://clawhub.ai/user/airix315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to list RunningHub apps, submit synchronous or asynchronous AI generation tasks, query task status, and route generated outputs to direct URLs or optional cloud storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe command and network handling could expose credentials, generated content, or the local agent account if the skill is misconfigured or invoked with hostile inputs.

Mitigation: Review the skill before installation, use it only with trusted prompts and configuration, keep RUNNINGHUB_BASE_URL set to an official RunningHub host, and avoid untrusted projectName or outputPath values until host validation and shell command handling are fixed.

Risk: Cloud storage mode can move generated outputs to Baidu Netdisk or Google Drive, which may be inappropriate for sensitive content.

Mitigation: Use cloud mode only for non-sensitive outputs and prefer direct RunningHub URLs when outputs do not need to be saved externally.

## Reference(s):

- [RHSkill ClawHub Release](https://clawhub.ai/airix315/skills/rhskill)
- [RHMCP](https://github.com/AIRix315/RHMCP)
- [RunningHub China](https://www.runninghub.cn)
- [RunningHub International](https://www.runninghub.ai)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [Shared Apps](references/shared-apps.json)
- [Configuration Template](references/config-template.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, JSON configuration, shell commands, and JSON task results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated task outputs may be returned as RunningHub URLs, local file paths, or cloud storage URLs depending on storage mode.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
