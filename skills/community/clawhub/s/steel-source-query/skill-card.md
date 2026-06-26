## Description: <br>
钢材货源查询 helps agents query steel spot prices, analyze price trends, manage supplier inventory, publish purchase or inventory records, import Excel inventory files, and prepare daily steel-market updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zgzymllm](https://clawhub.ai/user/zgzymllm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Steel traders, procurement teams, and business operators use this skill to look up steel prices, compare market trends, share inventory, publish purchase demand, and produce structured reports or spreadsheets for B2B steel trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle business inventory, buyer demand, supplier names, phone numbers, and other contact details. <br>
Mitigation: Require explicit user confirmation before publishing contact details, and define retention and deletion handling for local JSON data and uploaded Excel files. <br>
Risk: Shared Feishu publishing and scheduled push workflows can expose business data to unintended recipients if the target table or channel is not scoped correctly. <br>
Mitigation: Confirm who can access the target Feishu table and push destination before use, and replace the bundled table identifiers and push targets with deployment-specific values. <br>
Risk: External steel-price sources and cached market data may be incomplete, stale, or unavailable. <br>
Mitigation: Show source and timestamp information in responses, prefer fallback sources only when appropriate, and avoid treating generated trend analysis as investment or procurement advice without human review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zgzymllm/steel-source-query) <br>
- [Configuration template](references/config.template.json) <br>
- [Mysteel data source](https://www.mysteel.com) <br>
- [Lange Steel data source](https://www.lgmi.com) <br>
- [Feishu inventory table](https://my.feishu.cn/base/A27gbl3lDaheavs4sFhcO1K4ngg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands, JSON snippets, and generated Excel files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local JSON cache records, inventory files, purchase request files, and Excel imports or exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
