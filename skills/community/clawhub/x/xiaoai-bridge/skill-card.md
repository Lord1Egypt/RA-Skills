## Description: <br>
xiaoai-bridge connects Xiaomi XiaoAi speaker voice messages to an AI assistant workflow and can return responses through XiaoAi text-to-speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Warm-winter](https://clawhub.ai/user/Warm-winter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and smart home builders use this skill to route XiaoAi speaker voice commands into OpenClaw or another assistant workflow, then speak assistant responses back through the speaker. It is intended for Xiaomi IoT environments that can provide the required account and device credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes a Xiaomi session file and exposed tokens. <br>
Mitigation: Do not install this version as-is; remove scripts/.mi.json, revoke exposed Xiaomi tokens, and use only your own credentials. <br>
Risk: Credential requirements are not declared in metadata even though the skill needs Xiaomi account and device credentials. <br>
Mitigation: Declare required Xiaomi credentials before release and keep secrets in private environment variables or secret storage. <br>
Risk: The release includes unsafe copy-paste command examples using shell exec strings. <br>
Mitigation: Replace exec string examples with spawn or execFile calls that pass arguments as arrays. <br>
Risk: The lockfile uses HTTP package sources. <br>
Mitigation: Regenerate the lockfile with HTTPS package registry sources before installation. <br>
Risk: Voice command capture can expose private household speech or logs. <br>
Mitigation: Use a distinctive trigger phrase, private logs, and local access controls for any listener output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Warm-winter/xiaoai-bridge) <br>
- [MiGPT-Next API reference](references/migpt-api.md) <br>
- [MiGPT-Next project](https://github.com/idootop/migpt-next) <br>
- [passToken setup discussion](https://github.com/idootop/migpt-next/issues/4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JavaScript and shell command examples; the listener script emits newline-delimited JSON messages for voice commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Xiaomi account credentials, a XiaoAi device identifier, and Node.js 18 or newer. Runtime behavior depends on Xiaomi cloud access and polling interval configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
