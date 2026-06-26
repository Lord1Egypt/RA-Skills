## Description: <br>
Generate comprehensive SEO analysis reports from Google Search Console data with PDF export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgx-00](https://clawhub.ai/user/lgx-00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SEO operators, and site owners use this skill to collect Google Search Console data, analyze traffic trends, pages, queries, countries, and devices, and generate a PDF SEO report with recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Search Console service account credentials and potentially sensitive analytics data. <br>
Mitigation: Use a dedicated read-only service account, keep the JSON key out of chat and source control, and delete raw JSON and chart files after use if the data is sensitive. <br>
Risk: The bundled script includes fixed site URLs and hard-coded local input, chart, and PDF output paths. <br>
Mitigation: Inspect and edit the script before running it so the sites, input file, chart directory, and report output path match the current workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lgx-00/search-console-report) <br>
- [Google Search Console API Library](https://console.cloud.google.com/apis/library/searchconsole.googleapis.com) <br>
- [Google Search Console API OAuth scope](https://www.googleapis.com/auth/webmasters.readonly) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python code and shell commands; generated artifacts include JSON data, PNG charts, and a PDF report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Google Cloud service account key with Search Console read access and Python packages including pyjwt, cryptography, requests, matplotlib, pandas, and reportlab.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
