## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raidan-ai](https://clawhub.ai/user/raidan-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to log errors, corrections, knowledge gaps, and feature requests into local markdown learning files, then promote broadly useful findings into project memory or agent instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files can accidentally capture secrets, credentials, personal data, raw transcripts, or sensitive command output. <br>
Mitigation: Review entries before promotion and avoid storing sensitive information in learning files. <br>
Risk: Unreviewed learnings can introduce incorrect or misleading guidance into future agent sessions. <br>
Mitigation: Review and validate logged learnings before promoting them into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or similar persistent context files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raidan-ai/self-improving-agent-3-0-6) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local learning-entry formats and promotion guidance; users should review entries before adding them to persistent agent context.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
