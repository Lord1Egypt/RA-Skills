## Description: <br>
Searches and recommends Renesas semiconductor solutions for embedded system design using official Renesas product pages and datasheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangp-gh](https://clawhub.ai/user/wangp-gh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and embedded-system engineers use this skill to identify Renesas parts for applications such as BLE devices, MCUs, power management, sensors, and NFC, then verify parameters from official Renesas sources before making recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download Renesas datasheet PDFs into the current workspace. <br>
Mitigation: Use it in a workspace where local PDF files under embedded_dev/renesas/datasheet/ are acceptable, and remove old downloads when storage or workspace cleanliness matters. <br>
Risk: Datasheet recommendations could be wrong if values are copied from memory, product-page descriptions, or similar parts instead of official specification tables. <br>
Mitigation: Require each numerical parameter to come from an official Renesas product page or downloaded datasheet table, include source page or table citations, and mark unavailable values as not verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangp-gh/renesas-search) <br>
- [Server-resolved GitHub source](https://github.com/wangp-gh/renesas-search) <br>
- [Renesas product catalog](https://www.renesas.com/en/products) <br>
- [Renesas product families reference](references/product_families.md) <br>
- [Hermes install notes](HERMES_INSTALL.md) <br>
- [Test scenarios](TEST_SCENARIOS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown with tables, citations, local datasheet paths, and occasional bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download official Renesas datasheet PDFs to embedded_dev/renesas/datasheet/ in the current workspace.] <br>

## Skill Version(s): <br>
3.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
