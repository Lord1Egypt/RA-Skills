## Description: <br>
Analyzes Super Live, Taobao Live, and financial report files to calculate ROI, conversion, cost, revenue, and margin metrics and generate advertising performance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18262202398-star](https://clawhub.ai/user/18262202398-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing analysts and ecommerce operators use this skill to process local advertising and finance exports, compare performance across Super Live, Taobao Live, and financial data, and produce HTML or CSV reports for campaign review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read advertising and financial files from the configured input folder. <br>
Mitigation: Use a narrow input folder that contains only the intended CSV/XLSX files for the analysis period. <br>
Risk: Generated HTML reports may persist raw business data samples. <br>
Mitigation: Write reports to an explicit private output folder and review reports before sharing them. <br>
Risk: Untrusted CSV/XLSX files may be processed by the local Python runtime. <br>
Mitigation: Avoid running the skill on untrusted files and inspect source files before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18262202398-star/toufang-data-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [HTML reports, CSV summaries, terminal status text, and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local CSV/XLSX advertising and financial files from a configured folder and writes reports to a configured output folder.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
