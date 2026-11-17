## Description:

提供PPAP知识体系、文件模板生成、填写指导与检查校验；当用户需要了解PPAP流程、生成PPAP文件、填写提交保证书或检查文件完整性时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality, manufacturing, and supplier engineering users can use this Chinese-language skill to understand PPAP workflows, generate PPAP document templates, receive step-by-step filling guidance, and check PPAP package completeness. It is intended as documentation and workflow support, not as a substitute for customer-specific requirements or formal legal, certification, or safety decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PPAP requirements can vary by customer, and generated templates or reports may not satisfy every customer-specific requirement.

Mitigation: Review generated templates and checker reports against the applicable customer requirements before formal use.

Risk: The checker provides completeness and basic format checks, not a full validation of PPAP content accuracy.

Mitigation: Have qualified quality or supplier engineering reviewers verify the submitted PPAP content and supporting evidence.

Risk: The local checker reads user-provided JSON input and can write an output report when requested.

Mitigation: Run it only on PPAP JSON files intentionally provided for review and direct any output to expected local paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-ppap-guide)
- [Server-resolved GitHub source](https://github.com/duding-engicool/skill-ppap-guide)
- [PPAP file template guide](references/ppap_templates.md)
- [PPAP stage filling guide](references/ppap_guidance.md)
- [PPAP FAQ and cases](references/ppap_faq.md)
- [PPAP checker script](scripts/ppap_checker.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, generated document templates, shell command examples, and JSON or text checker reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The checker accepts PPAP information as a JSON file or JSON string and supports submission levels 1 through 5.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and release changelog reference 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
