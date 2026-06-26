## Description: <br>
Provides Xiaohongshu, XHS, and RedNote note details, metrics, and content analysis through SocialDataX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content researchers use this skill to fetch structured read-only details for Xiaohongshu/XHS/RedNote notes, including note content, author information, publish time, media, and interaction counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Returned Xiaohongshu note URLs may include xsec_token query parameters that preserve the exact openable link. <br>
Mitigation: Avoid forwarding or publishing full returned note URLs unless recipients should receive that exact link; prefer note_id or sanitized links when sharing outside the workspace. <br>


## Reference(s): <br>
- [SocialDataX API access](https://socialdatax.52choujiang.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-xhs-detail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY and node/npm for direct CLI use; data access is read-only.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
