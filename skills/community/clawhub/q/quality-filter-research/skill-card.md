## Description: <br>
Academic paper quality filtering agent with a scoring system and audit trail for research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nomorecoding](https://clawhub.ai/user/nomorecoding) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers and research workflow agents use this skill to score arXiv paper candidates for relevance and quality, separate passed and filtered papers, and keep a reviewable audit trail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit logs may retain paper lists, search parameters, scores, and filtering decisions. <br>
Mitigation: Use a normal project directory, avoid sensitive research inputs, and review or manage the log before sharing the workspace. <br>
Risk: The documented scoring criteria are tuned toward music or song generation and may under-rank papers from other research domains. <br>
Mitigation: Review the threshold and relevance criteria for the target domain and manually inspect filtered papers when recall matters. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown audit log with scoring rationale and optional shell-style usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends session records to research/{domain}/quality_filtering/quality_filtering_log.md when used as documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
