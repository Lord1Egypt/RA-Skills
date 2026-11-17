## Description:

YingDao-GuoKe helps an agent bind a Yingdao community profile link, store the profile UUID, and return community account, achievement, and developer activity statistics.

This skill is for research and development only.

## Publisher:

[guoke416](https://clawhub.ai/user/guoke416)

### License/Terms of Use:

MIT-0

## Use Case:

External Yingdao community users can use this skill to connect their profile UUID and ask an agent to summarize their Yingdao account, achievement, and development statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a Yingdao community profile UUID and derived personalId locally and uses them with Yingdao API endpoints.

Mitigation: Install only if comfortable sharing those identifiers with Yingdao APIs, and clear artifact/data/user.json to remove the binding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoke416/skills/yingdao-guoke)
- [ClawHub publisher profile](https://clawhub.ai/user/guoke416)
- [Yingdao community home page](https://www.yingdao.com/community/homePage)
- [Yingdao community profile example](https://www.yingdao.com/community/userCenter?userUuid=687223449269694466)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown-style text responses with account statistics and binding guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Yingdao profile UUID for repeated queries.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
