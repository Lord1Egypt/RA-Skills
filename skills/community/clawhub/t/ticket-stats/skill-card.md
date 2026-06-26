## Description: <br>
Analyzes internal support ticket spreadsheets, counts received, resolved, and late-response tickets, categorizes tickets by business-module keywords, and generates daily summary reports with charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FlankCat](https://clawhub.ai/user/FlankCat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal operations and support teams use this skill to summarize Excel or CSV ticket data, monitor daily ticket volume and response timeliness, and identify common business modules from keyword matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticket spreadsheets and generated reports may contain internal support details. <br>
Mitigation: Run the skill only on spreadsheets intended for summarization and store report and chart outputs in locations with appropriate internal access controls. <br>
Risk: Installing Python dependencies from untrusted sources can introduce supply-chain risk. <br>
Mitigation: Install pandas, openpyxl, and optional matplotlib only from trusted Python package sources. <br>
Risk: Keyword-based ticket classification can miss or misclassify issues when ticket language differs from the configured keyword lists. <br>
Mitigation: Review module labels and update keyword lists before using the summaries for operational decisions. <br>


## Reference(s): <br>
- [Ticket Stats on ClawHub](https://clawhub.ai/FlankCat/ticket-stats) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text report plus optional PNG chart files; guidance may include Markdown and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided Excel or CSV ticket spreadsheets and writes dated report and chart files to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
