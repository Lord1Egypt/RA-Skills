## Description:

生成标准SIPOC流程图（供应商-输入-流程-输出-客户）；当用户需要绘制过程流程图、梳理业务输入输出、建立跨部门流程映射或准备流程文档时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Business, quality, operations, and process-improvement users can use this skill to collect SIPOC elements, define process boundaries, and turn the result into a visual process map. It is suited for documenting supplier, input, process, output, and customer relationships for cross-functional review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub security summary says the generator can create unsafe HTML from untrusted SIPOC data or custom CSS.

Mitigation: Use only trusted SIPOC JSON and CSS, or sanitize and escape user-provided values before generating and opening the HTML output.

Risk: The generator accepts custom CSS and arbitrary output paths.

Mitigation: Prefer the bundled stylesheet and write outputs to a fixed, reviewed directory when running the skill in shared or automated environments.

Risk: The skill documentation describes PNG/PDF export, but the bundled export_sipoc.py file is empty.

Mitigation: Verify export behavior before relying on PNG or PDF deliverables, and use the generated HTML as the primary supported artifact unless export tooling is supplied.

## Reference(s):

- [SIPOC guide](references/sipoc-guide.md)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-sipoc-diagram)
- [Source repository](https://github.com/duding-engicool/skill-sipoc-diagram)
- [Server-resolved source commit](https://github.com/duding-engicool/skill-sipoc-diagram/tree/260e38bb427b7673dd38a817807a26857bbcc5f0)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)

## Skill Output:

**Output Type(s):** [guidance, text, json, html, shell commands]

**Output Format:** [Markdown guidance with SIPOC JSON examples and optional generated HTML diagram files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented PNG/PDF export path depends on scripts/export_sipoc.py, which is empty in the provided artifact.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
