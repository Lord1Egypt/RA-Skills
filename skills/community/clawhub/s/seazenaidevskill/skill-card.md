## Description: <br>
新城控股 AI 研发统筹技能——基于 Prompt-as-Code 的智能体系统。四阶段渐进式落地（Phase 1~4），每个 Phase 配套引导、操作手册和验收标准。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phoenixcastellan](https://clawhub.ai/user/phoenixcastellan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to install and maintain a prompt-as-code project orchestration scaffold for requirements, development, testing, and phase guidance. It also guides optional Feishu/Meegle setup for synchronizing requirements and task status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the skill creates a persistent .seazenai workflow scaffold and root prompt files that can change how agents operate in a repository. <br>
Mitigation: Install only in repositories where the team wants the .seazenai workflow scaffold and root prompt files. <br>
Risk: Enabled Feishu/Meegle synchronization can send requirement and task details and create or update remote work items automatically. <br>
Mitigation: Confirm the project_key, work item types, status mappings, and auto_sync setting before enabling synchronization. <br>


## Reference(s): <br>
- [Seazenaidevskill ClawHub release](https://clawhub.ai/phoenixcastellan/seazenaidevskill) <br>
- [研发统筹智能体 —— 详细落地方案（v3 参考版）](artifact/references/architecture.md) <br>
- [冷启动训练期设计](artifact/references/cold-start.md) <br>
- [Phase 1 知识提取执行手册（10 步）](artifact/references/knowledge-extraction.md) <br>
- [各 Phase 引导内容](artifact/references/phase-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, scaffold files, configuration templates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update persistent .seazenai workflow files and root prompt files in the target repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
