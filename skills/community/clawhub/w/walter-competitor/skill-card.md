## Description: <br>
Analyzes Amazon competitors by discovering top rival ASINs, comparing traffic sources and keywords, identifying weaknesses, and producing an advertising battle plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beyondbright](https://clawhub.ai/user/beyondbright) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace operators and Amazon sellers use this skill to turn a keyword and product price into competitor discovery, traffic analysis, keyword attack and defense guidance, weakness mapping, and budget scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: One script builds and runs shell commands from user-provided inputs, creating local command-execution risk. <br>
Mitigation: Review before installing and use only trusted keywords or ASINs until the mcporter wrapper avoids shell=True and validates inputs. <br>
Risk: Product, keyword, ASIN, traffic, and review-analysis queries may be sent to SellerSprite under the configured account. <br>
Mitigation: Use a dedicated, limited SellerSprite key where possible and avoid submitting sensitive product data unless disclosure is acceptable. <br>


## Reference(s): <br>
- [SIF Data Source Parsing Reference](references/data_parsing.md) <br>
- [SellerSprite MCP documentation](https://open.sellersprite.com/mcp/43) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with tables, prioritized action plans, budget scenarios, and inline command/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a required keyword and product price, with optional margin, to produce a single competitor-analysis plan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
