## Description: <br>
VectorBT A-share backtesting report generator that creates interactive HTML reports for single stocks and batch CSV/XLS/XLSX stock lists, with local TDX data and market-data fallback support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lotuspaladin-lab](https://clawhub.ai/user/lotuspaladin-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative analysts use this skill to generate VectorBT-based HTML backtesting reports for Chinese A-share tickers, either one stock at a time or from spreadsheet and CSV stock lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local TDX data directories and user-provided stock-list files. <br>
Mitigation: Run it only against intended local data paths and trusted CSV or Excel inputs. <br>
Risk: Generated report filenames and HTML can include names from user-provided CSV or Excel inputs. <br>
Mitigation: Use trusted input files and review generated reports before publishing or sharing them. <br>
Risk: The skill can contact third-party market-data services when local data is stale or missing. <br>
Mitigation: Use it in environments where those outbound market-data requests are permitted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lotuspaladin-lab/vbt-report) <br>
- [Publisher profile](https://clawhub.ai/user/lotuspaladin-lab) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates single-stock HTML reports and batch index pages; batch mode can read CSV, XLS, XLSX, or string-derived stock lists.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
