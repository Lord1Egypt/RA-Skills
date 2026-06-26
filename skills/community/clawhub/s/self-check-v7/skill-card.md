## Description: <br>
Self-Check System v7 guides agents through mandatory critical thinking, task decomposition, quality control, role separation, checkpoint logging, behavior tracking, and cross-agent memory synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eita19](https://clawhub.ai/user/eita19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to enforce a structured self-check workflow before delivery, including challenge prompts, alternatives comparison, quality gates, checkpoint logs, behavior tracking, and memory synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on checkpoint logging and behavior tracking can record task summaries, inferred preferences, and other interaction metadata. <br>
Mitigation: Confirm storage location, access, retention, deletion process, and whether logging can be disabled or scoped before installing. <br>
Risk: External memory synchronization through Bitable can share remembered items outside the local workspace. <br>
Mitigation: Require explicit consent for sync, verify the destination and access controls, and disable external sync when it is not needed. <br>
Risk: The mandatory governance workflow can change normal agent behavior for all tasks. <br>
Mitigation: Install only in environments that intentionally want strict pre-delivery checks, role separation, and review gates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eita19/self-check-v7) <br>
- [Y7 Framework reference](https://github.com/Y7-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with checklist templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require local checkpoint logs, behavior-tracker entries, and external memory-sync records.] <br>

## Skill Version(s): <br>
7.2.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
