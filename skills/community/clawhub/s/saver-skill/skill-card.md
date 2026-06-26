## Description: <br>
Saver is a Mainland China shopping assistant that helps agents analyze shopping needs, search JD.com and Taobao/Tmall products, compare prices, and return purchase links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyichu86](https://clawhub.ai/user/chenyichu86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use Saver to clarify shopping requirements, search supported Mainland China marketplaces, compare price and ranking signals, calculate effective costs, and return product recommendations with purchase links. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: Shopping searches are sent to a configured raw HTTP IP service, which can expose shopping intent to the service operator. <br>
Mitigation: Install only when the operator is trusted, and avoid using the skill for sensitive purchases or private shopping intent. <br>
Risk: The skill returns monetized affiliate product links while commission details are not shown to users. <br>
Mitigation: Ask the agent to clearly disclose affiliate links before presenting recommendations. <br>


## Reference(s): <br>
- [Saver on ClawHub](https://clawhub.ai/chenyichu86/saver-skill) <br>
- [chenyichu86 publisher profile](https://clawhub.ai/user/chenyichu86) <br>
- [Saver MCP server](http://81.70.235.20:3001/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls] <br>
**Output Format:** [Markdown product recommendations with linked product names, price details, and comparison context] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include affiliate purchase links and streaming progress updates.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact files describe 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
