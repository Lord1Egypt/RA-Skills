## Description:

Uniapp Guide provides practical uni-app cross-platform development guidance covering environment setup, project creation, configuration, lifecycle patterns, components, API calls, debugging, and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w333bao](https://clawhub.ai/user/w333bao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get concise guidance and examples for building, debugging, and releasing uni-app applications across web, mobile app, and mini program targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-pasted setup commands may fetch templates or packages that change over time.

Mitigation: Verify repository names and pin package or template versions where possible before running setup commands.

Risk: Running npm setup with elevated privileges can expand the impact of malicious or compromised packages.

Mitigation: Run package installation as a normal user in a project workspace rather than as an administrator.

Risk: Disabling WeChat URL checks outside local debugging can weaken request origin protections.

Mitigation: Keep WeChat urlCheck enabled for non-local and production builds.

Risk: Example API code reads a stored token and attaches it to requests.

Mitigation: Only send stored tokens to trusted API origins and adapt authentication handling before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/w333bao/skills/uniapp-guide)
- [uni-app Documentation](https://uniapp.dcloud.net.cn/)
- [uni-ui Components](https://uniapp.dcloud.net.cn/component/uniui/)
- [DCloud Community](https://ask.dcloud.net.cn/)
- [DCloud Plugin Marketplace](https://ext.dcloud.net.cn/)
- [HBuilderX](https://www.dcloud.io/hbuilderx.html)
- [WeChat Developer Tools](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides human-facing development guidance; generated examples should be reviewed before execution or production use.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
