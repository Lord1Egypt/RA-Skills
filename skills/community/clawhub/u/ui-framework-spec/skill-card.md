## Description:

UI Framework Spec guides agents to select, generate, review, and migrate UI code using framework-provided components from Element Plus, Ant Design, Arco Design, TDesign, and Semi Design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fize](https://clawhub.ai/user/fize)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to select among supported UI frameworks, generate framework-compliant Vue or React UI code, review code for framework compliance, and plan migrations between component systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated UI code may use locale assumptions that do not match the target project.

Mitigation: Review generated code for the locale the project actually needs, especially where examples show Chinese internationalization imports.

Risk: Framework API details may drift beyond the bundled reference summaries.

Mitigation: Check current official framework documentation when precise component props, version behavior, or migration details matter.

## Reference(s):

- [Framework Selection Guide](references/framework-selection.md)
- [Element Plus Reference](references/element-plus.md)
- [Ant Design Reference](references/ant-design.md)
- [Arco Design Reference](references/arco-design.md)
- [TDesign Reference](references/tdesign.md)
- [Semi Design Reference](references/semi-design.md)
- [Element Plus Documentation](https://element-plus.org)
- [Element Plus GitHub](https://github.com/element-plus/element-plus)
- [Ant Design Documentation](https://ant.design)
- [Ant Design GitHub](https://github.com/ant-design/ant-design)
- [Arco Design Documentation](https://arco.design)
- [Arco Design GitHub](https://github.com/arco-design/arco-design)
- [TDesign Documentation](https://tdesign.tencent.com)
- [TDesign GitHub](https://github.com/Tencent/tdesign)
- [Semi Design Documentation](https://semi.design)
- [Semi Design GitHub](https://github.com/DouyinFE/semi-design)
- [ClawHub Skill Page](https://clawhub.ai/fize/skills/ui-framework-spec)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions]

**Output Format:** [Markdown prose with framework-specific code snippets and review or migration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include framework recommendations, component code, compliance findings, migration plans, or theme and configuration guidance.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
