## Description: <br>
Automatically logs into the Jiangsu MSA integrated platform, queries meeting information for a specified date range, and exports structured meeting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tokido-25](https://clawhub.ai/user/tokido-25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized operators can use this skill to retrieve Jiangsu MSA meeting records for a date or date range and export fields such as time, location, attendees, and organizer. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Reusable government-platform credentials are embedded or provided as defaults. <br>
Mitigation: Remove and rotate the embedded password, and require authorized users to provide credentials through environment variables or another managed secret source. <br>
Risk: The skill can export sensitive meeting data to local Excel and JSON files. <br>
Mitigation: Document output paths and retention behavior, restrict access to generated files, and treat exported meeting records as sensitive. <br>
Risk: Dependencies are not pinned and Chrome WebDriver can be downloaded during first use. <br>
Mitigation: Pin and review dependencies and driver sources before routine deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tokido-25/xiaoqian) <br>
- [Jiangsu MSA integrated platform login](http://gchportal.js-msa.gov.cn/cas/login) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Guidance] <br>
**Output Format:** [Excel workbook (.xlsx), JSON export, and runtime log text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts optional start_date and end_date inputs; exported records include date, start time, meeting title, location, attendees, and organizer.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter lists 1.0.1 and _meta.json lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
