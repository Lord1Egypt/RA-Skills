## Description: <br>
Skill Privacy Guard helps agents detect and sanitize sensitive information in skill files before they are shared or published. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanggroot7](https://clawhub.ai/user/zhanggroot7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to review skill files for credentials, personal data, private infrastructure details, and other sensitive examples before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad sanitization rules can replace legitimate examples or miss some sensitive values. <br>
Mitigation: Keep version control or backups, review diffs before publishing, and manually inspect any high-impact credential or personal-data findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhanggroot7/skill-privacy-guard) <br>
- [Publisher profile](https://clawhub.ai/user/zhanggroot7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown status summary with sanitized-item counts and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports whether sensitive information was found and summarizes replacements or removals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
