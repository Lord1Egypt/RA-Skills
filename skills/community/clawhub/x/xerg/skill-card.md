## Description: <br>
Find wasted AI spend in OpenClaw, Hermes, and Cursor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xerg](https://clawhub.ai/user/xerg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Xerg to audit AI spend across OpenClaw, Hermes, and Cursor, identify waste patterns, and compare whether workflow or model changes reduced cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Xerg reads local AI usage logs, session transcripts, and Cursor exports that may contain sensitive prompts, responses, credentials, or business data. <br>
Mitigation: Keep audits local unless intentionally running connect, push, audit --push, or mcp-setup; review the CLI package or source before using it on sensitive data. <br>
Risk: Running npx @xerg/cli fetches and executes the published npm package before running Xerg. <br>
Mitigation: Review the package first and install a trusted version globally or run a local build when repeatability or source review is required. <br>
Risk: Remote OpenClaw audits can pull selected files to local temporary storage for analysis. <br>
Mitigation: Confirm the remote target and data scope before running remote audits, and handle temporary local audit data according to the environment's data policy. <br>


## Reference(s): <br>
- [Xerg documentation](https://xerg.ai/docs) <br>
- [Xerg source repository](https://github.com/xergai/xerg) <br>
- [@xerg/cli npm package](https://www.npmjs.com/package/@xerg/cli) <br>
- [Xerg homepage](https://xerg.ai) <br>
- [OpenSSH](https://www.openssh.com/) <br>
- [rsync](https://rsync.samba.org/) <br>
- [Railway CLI repository](https://github.com/railwayapp/cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local JSON audit output when the user runs Xerg audit commands.] <br>

## Skill Version(s): <br>
0.5.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
