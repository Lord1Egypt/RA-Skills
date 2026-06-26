## Description: <br>
为 Vibe coding 应用生成 AI 可读的中英文 DESIGN.md 设计系统，提供产品风格模板、九部分设计规范、组件样式、响应式规则和 Agent 提示指南。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agent builders use this skill to produce DESIGN.md design-system guidance for Vibe coding applications. It can generate product-inspired visual systems, component styling guidance, responsive rules, and prompt guidance for downstream UI generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator can overwrite a user-selected output file. <br>
Mitigation: Choose an explicit output path, review it before running generation, and keep backups for existing DESIGN.md files. <br>
Risk: Some marketing claims and template counts are broader than the generator-backed template list, and many templates are less complete than the highlighted professional examples. <br>
Mitigation: Treat generated DESIGN.md content as a design starting point and review the selected template for completeness before using it as team guidance. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lijinhongucl-pixel/vibe-coding-design-system) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Code audit report](artifact/CODE_AUDIT_REPORT.md) <br>
- [Template plan](artifact/TEMPLATES_PLAN.md) <br>
- [Improvement plan](artifact/IMPROVEMENT_PLAN.md) <br>
- [Custom configuration example](artifact/examples/custom_config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown DESIGN.md files with CSS/React snippets, command examples, and optional JSON configuration input] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python standard-library code; output files are written to user-selected paths and template completeness varies across the catalog.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
