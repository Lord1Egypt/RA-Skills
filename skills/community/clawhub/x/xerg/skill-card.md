## Description: <br>
Find wasted AI spend in OpenClaw, Hermes, and Cursor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xerg](https://clawhub.ai/user/xerg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Xerg to audit local OpenClaw, Hermes, and Cursor usage for wasted AI spend, compare workflow changes, and optionally push summarized audit results to Xerg Cloud. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The closed-source npm CLI reads local AI usage logs and session transcripts for cost analysis. <br>
Mitigation: Run local audit commands first, review the CLI's requested sources, and install only when that local file access matches the intended audit scope. <br>
Risk: Optional push, connect, and hosted MCP commands can send summarized audit results to Xerg Cloud. <br>
Mitigation: Use cloud sync only when intended, review remote or hosted setup before enabling it, and avoid push/connect features for local-only audits. <br>


## Reference(s): <br>
- [Xerg documentation](https://xerg.ai/docs) <br>
- [Xerg skill definition](https://xerg.ai/skill.md) <br>
- [@xerg/cli npm package](https://www.npmjs.com/package/@xerg/cli) <br>
- [Xerg homepage](https://xerg.ai) <br>
- [ClawHub skill page](https://clawhub.ai/xerg/skills/xerg) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, json] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON audit output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local audit results may include spend totals, rollups, findings, recommendations, comparison deltas, and source metadata.] <br>

## Skill Version(s): <br>
0.5.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
