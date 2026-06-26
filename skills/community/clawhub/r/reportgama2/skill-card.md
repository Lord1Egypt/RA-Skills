## Description: <br>
Generates deep market research reports for a target country and product category by combining multilingual search, news monitoring, competitor analysis, ecommerce pricing, ad-channel research, customs data, tender data, medical-registration lookups, social signals, charts, Markdown, and PDF export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxuan1992asia-svg](https://clawhub.ai/user/wangxuan1992asia-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to collect public market signals and produce structured country-and-category market research reports, especially for medical-device market intelligence and competitive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad public-web collection and fallback or estimated data can produce market claims that look more authoritative than they are. <br>
Mitigation: Independently verify official registry, pricing, hospital, customs, and market-share claims before using reports for business decisions. <br>
Risk: The skill installs Python dependencies, performs network collection, and writes local report files. <br>
Mitigation: Run it in an approved environment with controlled network access and an expected output directory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangxuan1992asia-svg/reportgama2) <br>
- [Publisher profile](https://clawhub.ai/user/wangxuan1992asia-svg) <br>
- [HS codes reference](artifact/references/hs_codes.md) <br>
- [Industry keywords reference](artifact/references/industry_keywords.md) <br>
- [UN Comtrade](https://comtrade.un.org) <br>
- [OEC](https://oec.world) <br>
- [Russian Federal Customs Service](http://www.customs.ru) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown reports, PDF exports, charts, tables, shell commands, and local output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report content may include estimated or fallback market data that requires independent verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json; artifact SKILL.md reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
