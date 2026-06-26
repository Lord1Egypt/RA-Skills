## Description: <br>
Cookie-based Twitter/X automation toolkit (timeline, notifications, posting, follow ops) for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GAN12003](https://clawhub.ai/user/GAN12003) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to connect OpenClaw-style agents to Twitter/X workflows for timeline review, notifications, signal analysis, posting, replies, follows, and related account operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent perform high-impact account actions such as public posts, follows, direct messages, subscription actions, password changes, or phone deletion. <br>
Mitigation: Disable unused high-impact code paths, require explicit confirmation or dry-run mode before mutating account state, and use test or low-risk accounts for evaluation. <br>
Risk: The skill relies on Twitter/X auth_token and ct0 session cookies, which can grant account access if exposed. <br>
Mitigation: Keep .env files private, avoid committing credentials, rotate any exposed session tokens, and restrict runtime access to only the accounts needed. <br>
Risk: The public summary does not fully surface the breadth of account, messaging, and purchase-related powers identified by the security evidence. <br>
Mitigation: Review the full artifact and security guidance before deployment, and document which account actions are enabled for each agent workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/GAN12003/twitter-api) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python code, shell commands, and JSON or text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and git; account access depends on auth_token and ct0 session cookies supplied through environment configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, released 2026-02-21T20:05:54Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
