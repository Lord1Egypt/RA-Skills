## Description: <br>
Researches Shanghai property bidding, award, and evaluation announcements, extracts project details from public PDFs with OCR, and calculates saturated property-management income. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[misbah-boop](https://clawhub.ai/user/misbah-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts researching Shanghai property-management projects use this skill to find public announcements, OCR PDFs, extract fee and project fields, and calculate saturated income or contract dates for named projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads public Shanghai property announcement PDFs and stores temporary PDF files locally. <br>
Mitigation: Run it in a working directory you control, review downloaded files, and clean up temporary PDFs after use. <br>
Risk: Batch scripts may write CSV output to a hard-coded local path. <br>
Mitigation: Change the CSV output path before running batch scripts so results are written only to an intended location. <br>
Risk: OCR can misread scanned announcement values used in fee and income calculations. <br>
Mitigation: Verify OCR-extracted dates, areas, fee standards, and calculated income against the source PDFs before relying on results. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/misbah-boop/shwuyeyanjiu) <br>
- [Shanghai property announcement list](https://962121.fgj.sh.gov.cn/wyweb/web/front/common/greenmorelist.jsp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell and Python code blocks, plus calculated project fields and summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on public PDF availability, local OCR tools, and manual review of OCR-derived numbers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
