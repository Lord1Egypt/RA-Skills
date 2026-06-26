## Description: <br>
Skill Polisher helps agents collect feedback, track skill health, check specification compliance, and produce improvement suggestions for agent skills without modifying other skill files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LuciusCao](https://clawhub.ai/user/LuciusCao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to monitor skill quality, collect ratings and comments, review health reports, and generate targeted improvement guidance for skills they choose to track. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents itself as read-only while persistently storing ratings, comments, expectations, tracking history, metrics, and suggestion files on disk. <br>
Mitigation: Treat it as a stateful local tracker, review the workspace storage location before use, and distinguish local data writes from the claim that it does not modify other skill files. <br>
Risk: Unusual skill names or force-style operations may create confusing tracking state or bypass normal safeguards. <br>
Mitigation: Use normal skill names, avoid force options unless necessary, and review generated reports or suggestions before acting on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/LuciusCao/skill-polisher) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [Best Practices](references/BEST-PRACTICES.md) <br>
- [Pitfalls](references/PITFALLS.md) <br>
- [Quality Standards](references/QUALITY-STANDARDS.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown reports and suggestions, JSON records, and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local feedback, expectations, tracking state, metrics, and suggestion history under the user's workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
