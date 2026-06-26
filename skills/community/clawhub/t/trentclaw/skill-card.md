## Description: <br>
Assess your Agent deployment against security risks using Trent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trent-ai-release](https://clawhub.ai/user/trent-ai-release) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit OpenClaw deployments, review configuration risks, and request deeper skill-package analysis from Trent after explicit upload confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends redacted OpenClaw configuration metadata and, after confirmation, packaged skill/source code to Trent. <br>
Mitigation: Use it only when that data sharing is acceptable, review the Phase 2 upload preview, and upload only after explicit confirmation. <br>
Risk: Secrets can be exposed if they are hard-coded in custom formats that are not recognized by the local redaction logic. <br>
Mitigation: Keep secrets in environment variables, review packaged skill contents when prompted, and rotate any credential suspected of exposure. <br>
Risk: Generated .skill archives can remain in the local workspace after packaging. <br>
Mitigation: Delete generated .skill archives when local packaged copies are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/trent-ai-release/trentclaw) <br>
- [Trent](https://trent.ai) <br>
- [Trent OpenClaw API key setup](https://trent.ai/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with inline bash and Python code blocks, severity-grouped findings, upload summaries, and configuration diff snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRENT_API_KEY and sends selected redacted configuration metadata and confirmed skill packages to Trent for analysis.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
