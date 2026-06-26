## Description: <br>
Legacy workaround for web_fetch fake-ip failures on older npm-global OpenClaw installs where Clash, Mihomo, or Surge fake-ip mode is blocked and the openclaw.json ssrfPolicy fix is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xing-xing-coder](https://clawhub.ai/user/xing-xing-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers maintaining older npm-global OpenClaw installs use this skill to inspect, apply, and revert a local workaround for web_fetch failures caused by fake-IP proxy environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying the workaround to an unexpected OpenClaw runtime could modify the wrong local JavaScript file. <br>
Mitigation: Run status and inspect before apply, confirm the target file is the expected npm-global OpenClaw runtime, and keep the generated backup files. <br>
Risk: The workaround is unnecessary on OpenClaw v2026.4.10 or later and may be less appropriate than the built-in configuration fix. <br>
Mitigation: Prefer the openclaw.json ssrfPolicy configuration on OpenClaw v2026.4.10 or later, and install this skill only for older npm-global OpenClaw versions affected by fake-IP web_fetch blocking. <br>


## Reference(s): <br>
- [Skill README](references/README.md) <br>
- [Patch Script](scripts/patch-openclaw-global-fakeip.sh) <br>
- [ClawHub Skill Page](https://clawhub.ai/xing-xing-coder/web-fetch-fakeip) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes status, inspect, apply, and revert flows for the local OpenClaw patch.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
