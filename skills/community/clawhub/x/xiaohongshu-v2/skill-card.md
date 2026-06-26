## Description: <br>
小红书自动化 V2 automates Xiaohongshu login, content publishing, search, feed review, and social interactions through Chrome DevTools Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TinaDu-AI](https://clawhub.ai/user/TinaDu-AI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Operators, creators, and developers can use this skill to manage Xiaohongshu account workflows from an agent-assisted CLI, including login checks, draft or live publishing, search discovery, and account interactions. It is best suited for controlled account operations where the user reviews content and understands platform and account risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logged-in Xiaohongshu automation can affect a real social account through posting, commenting, liking, and favoriting. <br>
Mitigation: Use a dedicated account, prefer fill-only workflows followed by manual review, and avoid unattended live posting. <br>
Risk: The security review notes anti-detection browser behavior and weakened Chrome sandbox settings. <br>
Mitigation: Run the skill in an isolated browser profile, VM, or other contained environment, and install it only when those platform and browser-security risks are acceptable. <br>
Risk: Session files and browser profiles may contain account access material. <br>
Mitigation: Keep cookies and profile directories private, restrict filesystem access, and delete session state when account access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TinaDu-AI/xiaohongshu-v2) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/TinaDu-AI) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON-like command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May operate a local Chrome browser profile and persist session state when account workflows are used.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
