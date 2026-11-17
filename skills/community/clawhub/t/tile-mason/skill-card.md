## Description:

瓦匠 is a Chinese-language tile masonry assistant that answers renovation questions about tile installation, waterproofing, leveling, materials, workmanship, acceptance checks, issue diagnosis, and cost estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangmeihaoaiya](https://clawhub.ai/user/zhangmeihaoaiya)

### License/Terms of Use:

MIT-0

## Use Case:

External users, homeowners, and entry-level tile workers use this skill to get Chinese-language guidance for tile masonry planning, material selection, construction checks, defect diagnosis, and local cost estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cost estimates and construction standards may vary by city, site conditions, contractor practices, and local regulations.

Mitigation: Treat estimates and standards as planning guidance and verify final decisions with local professionals or applicable regulations.

Risk: The skill may trigger on broad renovation terms that are adjacent to, but not specifically about, tile masonry.

Mitigation: Confirm the user question is about tile, masonry, waterproofing, leveling, or related cost estimation before relying on the response.

## Reference(s):

- [瓦匠常用材料对比参考](references/材料对比.md)
- [瓦匠工程验收标准参考](references/验收标准.md)
- [瓦匠施工工序参考](references/施工工序.md)
- [瓦匠成本估算参考](references/成本估算参考.md)
- [瓦匠常见问题与避坑指南](references/常见问题与避坑.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown responses with optional shell command examples and JSON cost-estimate output from the bundled calculator.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost-estimate outputs depend on user-provided room dimensions, tile specifications, price inputs, and city tier.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
