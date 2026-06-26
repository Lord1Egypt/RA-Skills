## Description: <br>
Provides WeChat mini-program CI commands for previewing, uploading, building npm assets, uploading cloud functions and storage, and retrieving SourceMaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[super9du](https://clawhub.ai/user/super9du) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to manage WeChat mini-program CI workflows, including local configuration checks, preview QR code generation, code upload, npm build steps, cloud asset uploads, and SourceMap retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The init workflow may install miniprogram-ci globally, changing the user's Node.js environment. <br>
Mitigation: Manually install and pin a trusted miniprogram-ci version before use, then review any global installation step before allowing it. <br>
Risk: The skill uses WeChat private key material and persists configuration under ~/.wxmini-ci.config.js. <br>
Mitigation: Store private keys with restricted filesystem permissions and review the configuration file before sharing logs, projects, or workspaces. <br>
Risk: Upload, cloud upload, and SourceMap commands can publish or retrieve remote project assets. <br>
Mitigation: Require explicit human approval and verify the target AppID, project, environment, version, and paths before running these commands. <br>


## Reference(s): <br>
- [miniprogram-ci npm package](https://www.npmjs.com/package/miniprogram-ci) <br>
- [WeChat miniprogram-ci documentation](https://developers.weixin.qq.com/miniprogram/dev/devtools/ci.html#%E6%A6%82%E8%BF%B0) <br>
- [ClawHub skill page](https://clawhub.ai/super9du/wx-miniprogram-ci) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration and CI output files when the described commands are executed.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and script constant) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
