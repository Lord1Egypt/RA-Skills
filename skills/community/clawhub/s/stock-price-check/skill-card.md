## Description: <br>
Query current A/HK/US-share stock prices using natural language stock names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silverfoxchina-gif](https://clawhub.ai/user/silverfoxchina-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up current A-share, Hong Kong, and US stock prices from natural-language company names or stock codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock queries contact external finance services. <br>
Mitigation: Use the skill only for simple stock-price lookups and avoid entering private account details or sensitive text as the query. <br>
Risk: The Python script imports the local requests package. <br>
Mitigation: Run it in a trusted Python environment with a trusted requests installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/silverfoxchina-gif/stock-price-check) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>
- [Sina Finance quote endpoint](https://hq.sinajs.cn/list={sina_code}) <br>
- [Eastmoney stock search endpoint](https://searchapi.eastmoney.com/api/suggest/get?input={stock_name}&type=14&count=5) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to external finance services; results depend on those services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
