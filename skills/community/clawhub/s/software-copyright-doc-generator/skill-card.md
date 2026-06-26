## Description: <br>
Generates Chinese software copyright application materials, including application form content, software manual text, and source-code submission guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grancy-zgs](https://clawhub.ai/user/grancy-zgs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers preparing Chinese software copyright registration materials use this skill to collect software details, draft application text, prepare user manual content, and receive source-code formatting guidance. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can automatically install an unpinned Python package when run. <br>
Mitigation: Install python-docx from a trusted source in a virtual environment before running the generator. <br>
Risk: Generated legal or application text may be incomplete or unsuitable for a specific submission. <br>
Mitigation: Review all generated copyright application materials before submitting them. <br>


## Reference(s): <br>
- [Software copyright source-code formatting requirements](references/源代码格式要求.md) <br>
- [Software copyright application form guidance](references/申请表填写说明.md) <br>
- [Software manual template](references/软件说明书模板.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown guidance and generated DOCX or Markdown document content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated application materials should be reviewed before submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
