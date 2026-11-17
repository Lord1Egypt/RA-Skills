## Description:

Generate and submit weekly reports from Aliyun DevOps workitems via EMOP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaojiangfeng](https://clawhub.ai/user/yaojiangfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations staff use this skill to generate, backfill, and submit weekly reports from Aliyun DevOps workitems to EMOP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses DevOps and EMOP tokens to read workitems and submit business reports.

Mitigation: Use least-privilege tokens, keep credentials in environment variables only, and review generated report content before submission.

Risk: Browser-session fallback can use an authenticated account when direct API access returns 403.

Mitigation: Use browser-session fallback only with an explicitly approved account and scope; prefer token-based API access when possible.

Risk: The artifact references local scripts that are outside the packaged skill evidence.

Mitigation: Inspect and pin the referenced local scripts before running the workflow with credentials present.

## Reference(s):

- [Project URLs and IDs](references/urls.md)
- [Local scripts and entrypoints](references/cli.md)
- [Aliyun DevOps project](https://devops.aliyun.com/projex/project/c9f4987bc93d5257fb041c0826/sprint/b1d7675f7b5e9ba57fe3284358#activeTab=Workitem&viewIdentifier=ead4d6570d314e123d03122ecd)
- [Aliyun DevOps workitem list API](https://devops.aliyun.com/projex/api/workitem/workitem/list?_input_charset=utf-8)
- [EMOP weekly report API](https://emop.oureman.com/api/weekly/report)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with HTML ordered-list content and API submission guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are 200-300 Chinese characters and are submitted as UTF-8 HTML ordered lists.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
