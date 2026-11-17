## Description:

Installs, checks, and verifies a Playwright plus Chromium browser automation environment with optional Xvfb-backed headed mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to prepare a host for Playwright browser automation, check system compatibility, install browser dependencies, and verify operation with screenshots in headless or Xvfb-backed headed mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged and mutable installation steps can modify the host by installing OS packages, global npm packages, and browser binaries.

Mitigation: Review before use on sensitive systems and run in a disposable container or VM where possible.

Risk: Verification and sharing workflows can create or upload screenshots that expose sensitive page content.

Mitigation: Avoid the Feishu upload example for sensitive screenshots, do not pass untrusted screenshot paths, and review screenshots before sharing.

Risk: Browser and virtual-display defaults include reduced isolation controls such as --no-sandbox and Xvfb -ac.

Mitigation: Pin or remove mutable global installs and tighten browser sandbox and Xvfb access settings before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/pw-browser-setup)
- [Baidu verification target](https://www.baidu.com)
- [Feishu image upload endpoint](https://open.feishu.cn/open-apis/im/v1/images)
- [Feishu message send endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create helper shell scripts and browser verification screenshots when commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
