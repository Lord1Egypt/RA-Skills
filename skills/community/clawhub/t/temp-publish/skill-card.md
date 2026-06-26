## Description: <br>
Skill Cortex helps an agent find, install, use, learn from, and release short-term skills when existing installed skills cannot complete a task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankwu001](https://clawhub.ai/user/ankwu001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to manage temporary OpenClaw capabilities on demand while keeping long-term installed skills separate. It is intended for workflows where an agent needs to search ClawHub, evaluate candidate skills, request approval, execute the selected skill, and clean up afterward. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search for, install, execute, uninstall, and remember third-party skills under broad agent judgment. <br>
Mitigation: Install it only when you intentionally want an agent to manage other skills, and review each proposed skill, publisher, source, and side-effect summary before approval. <br>
Risk: GitHub-sourced candidate skills and credential-using skills may carry higher supply-chain or data-exposure risk. <br>
Mitigation: Prefer server-resolved ClawHub candidates when possible, inspect GitHub-sourced candidates carefully, and do not approve credential use unless the requested access is necessary for the task. <br>
Risk: Reflex mode can reduce opportunities to review repeated actions. <br>
Mitigation: Use reflex mode only for stable read-only workflows, keep installation notifications visible, and downgrade to the standard confirmation path after any version change or failure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ankwu001/temp-publish) <br>
- [ClawHub](https://clawhub.ai) <br>
- [OpenClaw](https://github.com/openclaw) <br>
- [README](artifact/README.md) <br>
- [Design Document](artifact/DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose skill candidates, side-effect summaries, execution plans, recovery steps, and updates to local cortex memory.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
