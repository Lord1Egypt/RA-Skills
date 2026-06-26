## Description: <br>
Provides Chinese-language tile and masonry guidance for renovation questions, including tile installation, waterproofing, leveling, material selection, construction steps, acceptance checks, troubleshooting, and cost estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangmeihaoaiya](https://clawhub.ai/user/zhangmeihaoaiya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home renovators and tile or masonry workers use this skill to get practical Chinese-language guidance for tile work, waterproofing, material choices, quality checks, issue diagnosis, and rough cost estimation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad renovation wording and provide tile-specific guidance when the task is not actually tile or masonry related. <br>
Mitigation: Confirm that the user request is tile or masonry related before following specialized recommendations. <br>
Risk: Waterproofing, drainage, or structural recommendations can be sensitive to site conditions and local requirements. <br>
Mitigation: Use the guidance as planning or inspection support and confirm irreversible work with a qualified professional or applicable local standard. <br>
Risk: Cost estimates are approximate and depend on assumed labor rates, material prices, waste factors, and city tier. <br>
Mitigation: Replace defaults with current local quotes and measured dimensions before using estimates for budgeting or contracting. <br>


## Reference(s): <br>
- [瓦匠常见问题与避坑指南](references/常见问题与避坑.md) <br>
- [瓦匠成本估算参考](references/成本估算参考.md) <br>
- [瓦匠施工工序参考](references/施工工序.md) <br>
- [瓦匠常用材料对比参考](references/材料对比.md) <br>
- [瓦匠验收标准参考](references/验收标准.md) <br>
- [Tile cost estimation script](scripts/calc_tile.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with optional shell command examples and JSON cost-estimate output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cost estimates depend on user-supplied dimensions, tile specifications, tile price, city tier, and space type.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
