## Description: <br>
SKU对比分析 helps retail teams compare SKU performance across time periods, peer SKUs, sales metrics, inventory, AIoT conversion signals, and clerk-level selling performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail operators, analysts, and store teams use this skill to evaluate SKU trends, compare products in the same category or price band, and identify clerk performance patterns that affect sales and conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analysis results and console output can expose sensitive store sales, inventory, AIoT conversion, and clerk performance data. <br>
Mitigation: Use the skill only in a trusted retail workspace with an account scoped to the stores and SKU data intended for analysis. <br>
Risk: The skill depends on local API client code and the referenced sku-store-analysis skill. <br>
Mitigation: Verify the local API client and companion skill are trusted before using the skill with real retail data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gwyang7/retail-sku-comparison-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance, configuration] <br>
**Output Format:** [Python dictionaries with JSON-like fields plus console summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include store, SKU, sales, inventory, AIoT conversion, and clerk performance details from the connected retail data source.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
