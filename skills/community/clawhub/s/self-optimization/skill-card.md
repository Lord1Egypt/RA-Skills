## Description: <br>
Turn mistakes, corrections, dead ends, and repeated fixes into durable improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alethean-kaw](https://clawhub.ai/user/alethean-kaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture meaningful corrections, non-obvious failures, repeated friction, and missing capabilities, then promote stable lessons into durable guidance or reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learning entries can accidentally preserve secrets, customer data, private prompts, proprietary details, or sensitive personal and business context. <br>
Mitigation: Summarize lessons at a high level, remove sensitive details before saving, and review entries before promoting them into shared guidance. <br>
Risk: Promoted guidance or extracted skill scaffolds can encode incorrect lessons if the original incident was misunderstood. <br>
Mitigation: Review learning entries, require stable repeated patterns before promotion, and scan generated guidance or skill files before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alethean-kaw/self-optimization) <br>
- [Examples](references/examples.md) <br>
- [Hooks Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local learning files, guidance files, hook configuration, and skill scaffold files when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
