## Description: <br>
SSQ (Double Color Ball) lottery intelligent analysis fetches official draw data from cwl.gov.cn, computes hot/cold statistics, frequency distributions, AC values, odd-even ratios, and zone distributions, and can deliver five paid recommendation sets through clawtip payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinyu12166](https://clawhub.ai/user/jinyu12166) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch public SSQ draw data, generate local statistical lottery analysis, and optionally produce paid recommendation sets after clawtip payment validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lottery recommendations can be misread as predictive guarantees even though draws are random independent events. <br>
Mitigation: Treat generated recommendations as statistical analysis only and retain the skill's responsible-use warning that no method can guarantee winning. <br>
Risk: The skill performs outbound fetches and writes local database, report, and payment-order files. <br>
Mitigation: Install only when the user accepts the documented data flow and filesystem writes; use paid mode only after configuring the clawtip recipient address and SM4 key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinyu12166/skills/ssq-analyzer-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jinyu12166) <br>
- [China Welfare Lottery draw notice API](https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report and console text with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local SQLite draw database, a Markdown analysis report, and local clawtip order metadata when paid recommendations are requested.] <br>

## Skill Version(s): <br>
1.0.29 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
