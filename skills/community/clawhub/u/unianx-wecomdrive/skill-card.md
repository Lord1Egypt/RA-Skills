## Description:

Operates WeCom Docs and Drive through the official web interface for login checks, QR-code handoff, file export or download, local processing, report generation, and upload back to WeCom Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junjiantech](https://clawhub.ai/user/junjiantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to work with WeCom Drive or Tencent Docs links when browser login, document export, local analysis, generated reports, or upload back to WeCom Drive are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persistent browser helper can navigate to arbitrary URLs while logged in and return page details.

Mitigation: Use the skill only for expected WeCom or Tencent Docs workflows and avoid passing non-WeCom URLs unless a domain allowlist is added.

Risk: QR login screenshots, exported documents, generated reports, and uploaded results may contain private business content.

Mitigation: Keep QR codes and generated files private, share them only with intended users, and remove local outputs when the workflow is finished.

Risk: The local browser profile can preserve authenticated WeCom session state.

Mitigation: Clear the .state browser profile after use or when moving the skill between users or machines.

## Reference(s):

- [WeCom web workflow notes](artifact/references/wecom-web-notes.md)
- [WeCom Docs recent files](https://doc.weixin.qq.com/home/recent)
- [ClawHub skill page](https://clawhub.ai/junjiantech/skills/unianx-wecomdrive)
- [ClawHub homepage](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; helper scripts may produce JSON page summaries, QR screenshots, HTML reports, and DOCX reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; browser automation uses a persistent local profile for WeCom web sessions.]

## Skill Version(s):

0.0.1 (source: ClawHub release evidence; artifact frontmatter says 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
