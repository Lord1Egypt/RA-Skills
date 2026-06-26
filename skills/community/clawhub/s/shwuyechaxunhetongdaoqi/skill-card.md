## Description: <br>
Queries Shanghai property-management announcements to extract contract terms and award dates, calculate contract-expiry dates, and produce CSV results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[misbah-boop](https://clawhub.ai/user/misbah-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Property analysts, real estate operators, and developers use this skill to batch query Shanghai property-management project announcements by district or year and identify contracts that are expired or nearing expiry. <br>

### Deployment Geography for Use: <br>
China (Shanghai) <br>

## Known Risks and Mitigations: <br>
Risk: The end-to-end workflow depends on the separate shwuyeyanjiu skill and external Python packages. <br>
Mitigation: Review and install the required dependency skill and packages before running batch queries. <br>
Risk: Batch runs write CSV output files and may use a caller-selected output path. <br>
Mitigation: Choose an expected output path and review the generated CSV before using it for operational decisions. <br>
Risk: PDF download, OCR, and date extraction can leave some contract-expiry records incomplete or uncertain. <br>
Mitigation: Check source notes and failure reasons in the results, and verify important dates against the original announcements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/misbah-boop/shwuyechaxunhetongdaoqi) <br>
- [Shanghai property tender announcements](https://962121.fgj.sh.gov.cn/wyweb/web/front/common/greenmorelist.jsp) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and CSV result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CSV results can include project names, contract terms, award dates, calculated expiry dates, and source notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
