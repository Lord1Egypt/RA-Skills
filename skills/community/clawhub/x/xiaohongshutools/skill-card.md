## Description:

XiaoHongShu (Little Red Book) helps agents search and retrieve notes, profiles, comments, likes, feeds, and authenticated account interactions while generating the platform headers and cookies required for API requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chocomintx](https://clawhub.ai/user/chocomintx)

### License/Terms of Use:


## Use Case:

Developers and data analysts use this skill to collect XiaoHongShu content, inspect user, profile, and comment data, and perform account actions such as likes or follows when they have an authorized session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated use depends on web_session cookies that can grant account access.

Mitigation: Treat web_session as a password-equivalent secret, avoid sharing it in chat or logs, redact cookies from output, and rotate or revoke exposed sessions.

Risk: The skill can change account state through follow, like, comment, and delete actions.

Mitigation: Require explicit confirmation for every state-changing action and disable or wrap mutating calls when only collection or analysis is intended.

Risk: Automation against XiaoHongShu may create platform-policy, anti-abuse, rate-limit, or account restriction risk.

Mitigation: Use only authorized data and accounts, review platform rules before deployment, rate-limit requests, avoid unnecessary concurrency, and stop when restriction or abuse signals appear.

Risk: The security guidance identifies eval() configuration parsing and unpinned dependencies as pre-use concerns.

Mitigation: Replace eval() configuration parsing with a safe parser and pin dependencies before installing or running the skill.

Risk: The security guidance calls out an underdocumented read-count metrics flow.

Mitigation: Remove or disable the read-count metrics flow before production use unless it has been reviewed and explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chocomintx/skills/xiaohongshutools)
- [RedCrack upstream reference](https://github.com/Cialle/RedCrack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API usage examples, cookie and proxy configuration, and risk-aware operating guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
