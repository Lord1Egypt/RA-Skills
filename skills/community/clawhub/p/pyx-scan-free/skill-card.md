## Description: <br>
技能安全扫描(免费版) scans registered AI skills through the Scanner API and returns trust, risk, confidence, and issue-report summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and automation teams use this skill to request Scanner API checks for one or more registered AI skills and summarize trust scores, risk scores, confidence, and reported issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests local read, exec, and write authority even though the documented workflow mostly calls an external Scanner API. <br>
Mitigation: Review requested permissions before installation and prefer a release that removes or scopes write access for scanner-only use. <br>
Risk: The skill under-documents what skill names, callback URLs, or related inputs are sent to the external scanner service. <br>
Mitigation: Avoid confidential internal skill names and callback URLs unless sending them to the scanner service is acceptable. <br>
Risk: Clawscan marked the release suspicious. <br>
Mitigation: Perform manual review before deployment and treat scanner results as advisory until the skill's permissions and external data handling are documented. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pyx-scan-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Scanner API endpoint](https://scanner.pyxmate.com/api/v1/check/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with optional JSON excerpts and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task status, parsed score summaries, issue details, and error information when requests fail.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
