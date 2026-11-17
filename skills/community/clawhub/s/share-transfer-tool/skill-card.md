## Description:

Cloud Share Downloader helps an agent detect supported cloud-share and short-video links, attempt automated retrieval, and return transfer guidance or a new share link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to process supported cloud-storage or short-video share links, identify the provider, and receive automated download or transfer guidance. For providers requiring account authorization, the skill may ask for cloud-storage cookies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may request reusable cloud-storage cookies that can act like account session credentials.

Mitigation: Do not paste cloud-storage cookies into chat or agent workflows; prefer delegated authorization and review credential handling before use.

Risk: Automated saving and re-sharing can copy content outside its original sharing context.

Mitigation: Use only with non-sensitive content that the user is authorized to copy and re-share, and confirm storage, sharing, retention, and deletion behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sxliuyu/skills/share-transfer-tool)
- [Publisher Profile](https://clawhub.ai/user/sxliuyu)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with JSON-like status objects and URLs when transfer succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request cloud-storage cookies for Baidu, Aliyun, or other providers that require account authorization.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
