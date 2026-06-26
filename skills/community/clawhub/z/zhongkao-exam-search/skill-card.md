## Description: <br>
Searches for, downloads, and verifies Zhongkao Chinese high school entrance exam papers across regions, subjects, and years in China. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abill6688](https://clawhub.ai/user/abill6688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, parents, tutors, and education-support agents use this skill to locate Zhongkao exam papers by region, subject, and year, then download and validate candidate files before using or uploading them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and extracts exam-paper files from multiple external sites, including lower-trust social-media and cloud-drive sources. <br>
Mitigation: Review before installing, confirm each URL and output path, use only a dedicated download folder, scan downloaded files, and extract archives in an isolated directory. <br>
Risk: Downloaded files may be incomplete, redirected HTML pages, archives, or unverified documents that should not be reused automatically. <br>
Mitigation: Run the verification workflow and do not upload anything to a knowledge base until verification succeeds. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abill6688/zhongkao-exam-search) <br>
- [Server-resolved publisher profile](https://clawhub.ai/user/abill6688) <br>
- [Zhongkao source reference](artifact/references/sources.md) <br>
- [Edge-case handling reference](artifact/references/edge-cases.md) <br>
- [Zhongkao.com](https://www.zhongkao.com) <br>
- [Zhongxue English exam list](https://trjlseng.com/zkst/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON script output and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded exam-paper files for user-selected region, subject, year, and answer-version criteria.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
