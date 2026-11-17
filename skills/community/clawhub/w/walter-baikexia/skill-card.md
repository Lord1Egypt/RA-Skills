## Description:

蜗牛公司百科虾技能包。为员工解答公司相关问题（制度、福利、流程、组织架构等）。当用户询问公司相关问题时触发。知识库没有的问题一律不答，不编造，不联网搜索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[beyondbright](https://clawhub.ai/user/beyondbright)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill to ask company-specific questions about policies, benefits, workflows, organization structure, onboarding, and frequently asked procedures. Administrators can synchronize the Feishu knowledge base and manage local cache status for the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use local Feishu credentials to send messages and upload local files with weak path and account controls.

Mitigation: Use a dedicated least-privilege Feishu app account, restrict who can run sync and messaging scripts, and patch path containment, account fallback, redirect-token handling, and verbose logging before production use.

Risk: Untrusted synchronized wiki content can contain MEDIA markers that influence which local files are uploaded.

Mitigation: Reject untrusted wiki content, validate MEDIA entries against expected cache directories, and review synchronized content before enabling automated Feishu sends.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beyondbright/skills/walter-baikexia)
- [蜗牛大百科 Feishu wiki](https://campsnail.feishu.cn/wiki/VGRRw7s4BiStank4GnpczxnGn44)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or Markdown with optional Feishu mention tags, MEDIA references, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are intended to be grounded in synchronized knowledge-base content and may be sent through Feishu messaging scripts when mentions or media are present.]

## Skill Version(s):

2.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
